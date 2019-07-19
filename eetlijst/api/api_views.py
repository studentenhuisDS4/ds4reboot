import traceback
from datetime import timedelta
from decimal import Decimal

from django.db.models import Sum, Case, When, Value, F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import log_validation_errors, log_exception, illegal_action, success_action, Map
from eetlijst.api.api import DinnerSchema, UserDinnerSchema
from eetlijst.models import Dinner, UserDinner
from user.models import Housemate

DINNER_CLOSED_MESSAGE = "This dinner has been closed. It needs to be opened again to adjust it"


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Dinner.objects.order_by('-date')
    serializer_class = DinnerSchema

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        dinner = self.get_object()
        house_balance_unshare = None

        try:
            # actual action
            if dinner.cook == request.user:
                if dinner.num_eating <= 1:
                    # TODO easter egg
                    return illegal_action(
                        "(Sven, is that you?) Cant cook for yourself. ## Annoyed-server badge awarded ##."
                            .format(cook=dinner.cook.housemate.display_name))
                if dinner.open:
                    dinner.open = False
                    dinner.close_time = timezone.now()
                else:
                    if dinner.cost:
                        house_balance_unshare = self.__unshare_costs(dinner)
                        dinner.cost = None
                    dinner.open = True
                    dinner.close_time = None
                dinner.save()

                return success_action(data={
                    'house_balance_unshare': house_balance_unshare,
                    'dinner': DinnerSchema(dinner).data,
                }, status=status.HTTP_202_ACCEPTED)
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
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    @action(detail=True, methods=['post'])
    def cost(self, request, pk=None):
        dinner = self.get_object()
        house_balance_before = None

        try:
            result = DinnerSchema().load(data=request.data, partial=("eta_time",))  # validation only, never save
            if result.errors:
                return log_validation_errors(result.errors)

            # actual action
            if dinner.cook:
                if dinner.open:
                    return illegal_action(
                        "Dinner is still open. Close it before sharing costs.")
                else:
                    if dinner.cost:
                        house_balance_before = self.__unshare_costs(dinner)
                        dinner.cost = None
                        dinner.cost_time = None
                    house_balance = self.__share_costs(dinner, result.data['cost'])
                    dinner.cost = result.data['cost']
                    dinner.cost_time = timezone.now()
                    dinner.save()

                return success_action(data={
                    'house_balance_before': house_balance_before,
                    'house_balance': house_balance,
                    'dinner': DinnerSchema(dinner).data,
                }, status=status.HTTP_202_ACCEPTED)
            else:
                if dinner.cook:
                    # TODO easter egg
                    return illegal_action(
                        "{cook} is signed up as cook, so this user must set the food costs.".format(
                            cook=dinner.cook.housemate.display_name))
                else:
                    # TODO easter egg
                    return illegal_action(
                        "No user is signed up as cook... you hacker.")
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    ###
    # action:       eta_time
    # function:     set an eta_time
    # restriction:  user needs to be cook
    ###
    @action(detail=True, methods=['post'])
    def eta_time(self, request, pk=None):
        dinner = self.get_object()

        try:
            serializer = DinnerSchema(data=request.data, exclude=('cost',))
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)
            else:
                if not dinner.cook:
                    return illegal_action("Set yourself as cook before setting the ETA.")
                elif dinner.cook.id is not request.user.id:
                    return illegal_action("Only {name} can set an ETA (as he/she is cook).".format(
                        name=dinner.cook.housemate.display_name))
                else:
                    dinner.eta_time = Map(request.data).eta_time
                    dinner.save()

                    serializer = DinnerSchema(dinner)
                    serializer.data['eta_time'] = dinner.eta_time
                    return success_action(serializer.data)

        except Exception as e:
            return log_exception(e, traceback.format_exc())

    def __share_costs(self, dinner, cost):
        dinner_uds = dinner.userdinner_set.all()

        # update housemate objects for users who signed up
        house_hm = Housemate.objects.get(display_name='Huis')
        remainder = house_hm.balance
        split_cost = Decimal(round((cost - remainder) / dinner.num_eating, 2))
        house_hm.balance = dinner.num_eating * split_cost - cost + remainder

        # update userdinner set belonging to dinner
        for dinner_ud in dinner_uds:
            hm = dinner_ud.user.housemate
            hm.balance -= dinner_ud.count * split_cost
            dinner_ud.split_cost = -1 * dinner_ud.count * split_cost

            if dinner_ud.is_cook:
                hm.balance -= split_cost - cost
                dinner_ud.split_cost = cost - split_cost * (1 + dinner_ud.count)

            dinner_ud.save()
            hm.save()
        house_hm.save()

        # TODO check balances and LOG to file
        return house_hm.balance

    def __unshare_costs(self, dinner):
        dinner.userdinner_set.all()

        # Reverse existing costs
        cost_revert = -dinner.cost

        # update housemate objects for users who signed up
        house_hm = Housemate.objects.get(display_name='Huis')
        remainder = house_hm.balance
        split_cost_inv = Decimal(round((cost_revert - remainder) / dinner.num_eating, 2))
        house_hm.balance = dinner.num_eating * split_cost_inv - cost_revert + remainder

        dinner_uds = dinner.userdinner_set.all()
        for dinner_ud in dinner_uds:
            hm = dinner_ud.user.housemate
            hm.balance -= dinner_ud.count * split_cost_inv
            if dinner_ud.is_cook:
                hm.balance += cost_revert - split_cost_inv
            dinner_ud.split_cost = None
            dinner_ud.save()
            hm.save()
        house_hm.save()

        # TODO check balances and LOG to file
        return house_hm.balance


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
            user_dinner, created = serializer.save()

            # actual action
            if user_dinner.dinner.open:
                user_dinner.count += 1
                user_dinner.save()
                dinner = self.__update_dinner(user_dinner)
                if created:
                    self.return_status = status.HTTP_201_CREATED
                return success_action(DinnerSchema(dinner).data, self.return_status)
            else:
                return illegal_action(DINNER_CLOSED_MESSAGE, data=DinnerSchema(user_dinner.dinner).data)
        except Exception as e:
            return log_exception(e, tb=traceback.format_exc())

    @action(detail=False, methods=['post'])
    def signoff(self, request):
        self.return_status = self.default_status

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)
            user_dinner, created = serializer.save()

            # actual action
            if user_dinner.dinner.open:
                user_dinner.count = 0
                user_dinner.save()
                dinner = self.__update_dinner(user_dinner)
                if created:
                    self.return_status = status.HTTP_201_CREATED
                return success_action(DinnerSchema(dinner).data, self.return_status)
            else:
                return illegal_action(DINNER_CLOSED_MESSAGE, data=DinnerSchema(user_dinner.dinner).data)
        except Exception as e:
            return log_exception(e, tb=traceback.format_exc())

    @action(detail=False, methods=['post'])
    def cook(self, request):
        self.return_status = self.default_status

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)
            user_dinner, created = serializer.save()

            # actual action
            if user_dinner.dinner.open:
                if request.data.get('sign_off'):
                    user_dinner.is_cook = False
                else:
                    cook_dinner = UserDinner.objects.filter(dinner_date=user_dinner.dinner_date, is_cook=True).first()
                    if cook_dinner is None or cook_dinner.user.id == user_dinner.user.id:
                        user_dinner.is_cook = not user_dinner.is_cook
                        user_dinner.save()
                    else:
                        return illegal_action(
                            "{cook} is already signed up as cook.".format(cook=cook_dinner.user.housemate.display_name))
                dinner = self.__update_dinner(user_dinner)
                return success_action(DinnerSchema(dinner).data, self.return_status)
            else:
                return illegal_action(DINNER_CLOSED_MESSAGE, data=DinnerSchema(user_dinner.dinner).data)
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
        # if SQL count > 0
        if ud_annotated['sum_count']:
            cook_ud = user_dinners.filter(is_cook=True).first()

            dinner = Dinner.objects.get(date=input_ud.dinner_date)
            dinner.num_eating = ud_annotated['sum_count']
            if cook_ud:
                dinner.cook = cook_ud.user
                if dinner.cook_signup_time is None:
                    dinner.cook_signup_time = timezone.now()
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
