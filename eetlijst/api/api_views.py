import traceback
from datetime import timedelta

from django.db.models import Sum
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import log_validation_errors, log_exception, Map
from eetlijst.api.api import DinnerSchema, UserDinnerSchema
from eetlijst.models import Dinner, UserDinner


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Dinner.objects.order_by('-date')
    serializer_class = DinnerSchema


class UserDinnerViewSet(ListModelMixin, GenericViewSet):
    queryset = UserDinner.objects.order_by('-dinner_date')
    serializer_class = UserDinnerSchema

    default_status = status.HTTP_200_OK
    return_status = default_status

    @action(detail=False, methods=['post'])
    def signup(self, request):
        self.return_status = self.default_status

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)

            # actual action
            user_dinner, created = serializer.save()
            user_dinner.count += 1
            user_dinner.save()
            dinner, user_dinners = self.__update_dinner(user_dinner)

            if created:
                self.return_status = status.HTTP_201_CREATED

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                     'user_dinners': UserDinnerSchema(user_dinners, many=True, exclude=['dinner']).data
                 }},
                status=self.return_status)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return log_exception(e)

    @action(detail=False, methods=['post'])
    def signoff(self, request):
        self.return_status = self.default_status

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)

            # actual action
            user_dinner, created = serializer.save()
            user_dinner.count = 0
            user_dinner.save()

            dinner, user_dinners = self.__update_dinner(user_dinner)
            if created:
                self.return_status = status.HTTP_201_CREATED

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                     'user_dinners': UserDinnerSchema(user_dinners, many=True, exclude=['dinner']).data
                 }},
                status=self.return_status)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            return log_exception(e)

    def __update_dinner(self, input_ud):
        # Collect and update
        user_dinners = UserDinner.objects.filter(dinner_date=input_ud.dinner_date)
        user_dinners.filter(count__exact=0).delete()

        total = user_dinners.aggregate(total=Sum('count'))['total']
        dinner = None
        if total:
            dinner, created_dinner = Dinner.objects.get_or_create(date=input_ud.dinner_date)
            dinner.num_eating = total
            dinner.save()
            user_dinners.update(dinner=dinner)
        else:
            Dinner.objects.filter(date=input_ud.dinner_date).delete()

        return dinner, user_dinners


# Week list
class DinnerWeekViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = DinnerSchema
    queryset = Dinner.objects.order_by('-date')

    def get_queryset(self):
        """
        This view should return a list of all dinners
        entered this week.
        """
        return Dinner.objects \
            .filter(date__gte=datetime.now() - timedelta(days=datetime.now().weekday())) \
            .filter(date__lte=datetime.now() + timedelta(days=(7 - datetime.now().weekday()))) \
            .order_by('date')
