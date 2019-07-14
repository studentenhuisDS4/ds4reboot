import traceback
from datetime import timedelta

from django.db.models import Sum, Count, Case, When, Value
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import log_validation_errors, log_exception, Map, illegal_action
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
            dinner = self.__update_dinner(user_dinner)

            if created:
                self.return_status = status.HTTP_201_CREATED

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
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
            dinner = self.__update_dinner(user_dinner)

            if created:
                self.return_status = status.HTTP_201_CREATED

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                 }},
                status=self.return_status)
        except Exception as e:
            return log_exception(e, tb=traceback.format_exc())

    @action(detail=False, methods=['post'])
    def cook(self, request):
        self.return_status = self.default_status

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)

            # actual action
            user_dinner, created = serializer.save()
            if request.data.get('signoff') and request.data['signoff']:
                user_dinner.is_cook = False
            else:
                ddate = user_dinner.dinner_date
                cook_dinner = UserDinner.objects.filter(dinner_date=ddate, is_cook=True).first()
                if cook_dinner is None or cook_dinner.user == user_dinner.user:
                    user_dinner.is_cook = not user_dinner.is_cook
                    user_dinner.save()
                else:
                    return illegal_action(
                        "{cook} is already signed up as cook.".format(cook=cook_dinner.user.housemate.display_name))

            dinner = self.__update_dinner(user_dinner)
            if created:
                self.return_status = status.HTTP_201_CREATED

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                 }},
                status=self.return_status)
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    def __update_dinner(self, input_ud):
        # Collect and update
        user_dinners = UserDinner.objects.filter(dinner_date=input_ud.dinner_date)
        final_ud = user_dinners.annotate(sum_count=Count(
            Case(
                When(is_cook=True, then=Value(1)), When(count__gt=0, then='count'),
                default=Value(0),
            )))

        total = final_ud.aggregate(total=Sum('sum_count'))['total']
        dinner = None
        if total:
            cook_ud = user_dinners.filter(is_cook=True).first()

            dinner, created_dinner = Dinner.objects.get_or_create(date=input_ud.dinner_date)
            dinner.num_eating = total
            if cook_ud:
                dinner.cook = cook_ud.user
            else:
                dinner.cook = None
            dinner.save()
            user_dinners.update(dinner=dinner)
        else:
            Dinner.objects.filter(date=input_ud.dinner_date).delete()

        return dinner


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
