import traceback
from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum, Case, When, Value, F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import log_validation_errors, log_exception, illegal_action
from eetlijst.api.api import DinnerSchema, UserDinnerSchema
from eetlijst.models import Dinner, UserDinner
from user.models import Housemate


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Dinner.objects.order_by('-date')
    serializer_class = DinnerSchema

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        dinner = self.get_object()

        # actual action
        try:
            if dinner.cook == request.user:
                if dinner.num_eating <= 1:
                    # TODO easter egg
                    return illegal_action(
                        "(Sven, is that you?) Stop fucking around and get back to cramming exams. Jeez.".format(
                            cook=dinner.cook.housemate.display_name))
                if dinner.open:
                    dinner.open = False
                    dinner.close_time = timezone.now()
                else:
                    # unshare costs
                    dinner.open = True
                    dinner.close_time = None
                dinner.save()
            else:
                if dinner.cook:
                    # TODO easter egg
                    return illegal_action(
                        "{cook} is signed up as cook, so this user must close the list.".format(
                            cook=dinner.cook.housemate.display_name))
                else:
                    # TODO easter egg
                    return illegal_action(
                        "No user is signed up as cook, so the list can't be closed.")

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                 }},
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    @action(detail=True, methods=['post'])
    def cost(self, request):
        dinner = self.get_object()

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)

            # actual action
            if dinner.cook:
                if dinner.open:
                    return illegal_action(
                        "Dinner is still open. Close it before sharing costs.")
                else:
                    # share costs here
                    dinner.cost =
                dinner.save()
            else:
                if dinner.cook:
                    return illegal_action(
                        "{cook} is signed up as cook, so this user set the food costs.".format(
                            cook=dinner.cook.housemate.display_name))
                else:
                    # TODO easter egg
                    return illegal_action(
                        "No user is signed up as cook... you hacker.")

            return Response(
                {'status': 'success',
                 'result': {
                     'dinner': DinnerSchema(dinner).data,
                 }},
                status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    def __share_costs(self, dinner, cost):
        dinner.userdinner_set.all()

    def __unshare_costs(self, dinner):
        dinner.userdinner_set.all()

        # Reverse existing costs
        cost_amount = -dinner.cost

        # update housemate objects for users who signed up
        huis = Housemate.objects.get(display_name='Huis')
        remainder = huis.balance
        split_cost = Decimal(round((cost_amount - remainder) / dinner.num_eating, 2))
        huis.balance = dinner.num_eating * split_cost - cost_amount + remainder

        for u in users_enrolled:
            h = Housemate.objects.get(user=u.user)

            h.balance -= u.count * split_cost

            if u.is_cook:
                h.balance -= split_cost

            u.split_cost = None

            u.save()
            h.save()

        huis.save()


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
        user_dinners.filter(Q(is_cook=False) & Q(count__exact=0)).delete()

        ud_annotated = user_dinners.aggregate(sum_count=Sum(
            Case(
                When(is_cook=False, then=F('count')), When(is_cook=True, then=Value(1) + F('count')),
                default=Value(0),
            )))

        dinner = None
        if ud_annotated['sum_count']:
            cook_ud = user_dinners.filter(is_cook=True).first()

            dinner, created_dinner = Dinner.objects.get_or_create(date=input_ud.dinner_date)
            dinner.num_eating = ud_annotated['sum_count']
            if cook_ud:
                dinner.cook = cook_ud.user
                if dinner.cook_signup_time is None:
                    dinner.cook_signup_time = timezone.localtime()
            else:
                dinner.cook = None
                dinner.cook_signup_time = None
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
            .filter(date__gte=timezone.now() - timedelta(days=timezone.now().weekday())) \
            .filter(date__lte=timezone.now() + timedelta(days=(7 - timezone.now().weekday()))) \
            .order_by('date')
