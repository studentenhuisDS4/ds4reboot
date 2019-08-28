import traceback
from datetime import timedelta

from django.db.models import Sum, Case, When, Value, F, Q
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import log_validation_errors, log_exception, illegal_action, success_action, Map
from eetlijst.api.serializers.dinner import DinnerSchema, UserDinnerSchema
from eetlijst.models import Dinner, UserDinner

DINNER_CLOSED_MESSAGE = "This dinner has been closed. It needs to be opened again to adjust it"


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Dinner.objects.order_by('-date')
    serializer_class = DinnerSchema
    pagination_class = LimitOffsetPagination
    filter_fields = '__all__'

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        dinner = self.get_object()

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
                        dinner.unshare_cost()
                    dinner.open = True
                    dinner.close_time = None
                dinner.save()

                return success_action(data=DinnerSchema(dinner).data, status=status.HTTP_202_ACCEPTED)
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

        try:
            result = DinnerSchema().load(data=request.data, partial=("eta_time",))  # validation only, never save
            if 'errors' in result:
                return log_validation_errors(Map(result).errors)

            uds = dinner.userdinner_set.all()
            for ud in uds:
                if not ud.user.is_active:
                    return log_validation_errors(
                        {'is_active': f'{ud.user.housemate.display_name} is not active anymore. '
                                      f'Remove him to fix this error.'})
            # actual action
            if dinner.cook:
                if dinner.open:
                    return illegal_action(
                        "Dinner is still open. Close it before sharing costs.")
                else:
                    if dinner.cost:
                        dinner.unshare_cost()
                    dinner.share_cost(result['cost'])
                    dinner.save()
                return success_action(data=DinnerSchema(dinner).data, status=status.HTTP_202_ACCEPTED)
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


class UserDinnerViewSet(ListModelMixin, GenericViewSet):
    queryset = UserDinner.objects.order_by('-dinner_date')
    serializer_class = UserDinnerSchema
    pagination_class = LimitOffsetPagination

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
        signoff = None
        if 'sign_off' in request.data:
            signoff = request.data.pop('sign_off')

        try:
            serializer = UserDinnerSchema(data=request.data)
            if not serializer.is_valid():
                return log_validation_errors(serializer.errors)
            user_dinner, created = serializer.save()

            # actual action
            if user_dinner.dinner.open:
                if signoff:
                    user_dinner.is_cook = False
                else:
                    cook_dinner = UserDinner.objects.filter(dinner_date=user_dinner.dinner_date, is_cook=True).first()
                    if cook_dinner is not None and cook_dinner.id != user_dinner.id:
                        user_dinner.is_cook = True
                        cook_dinner.is_cook = False
                        cook_dinner.save()
                    else:
                        user_dinner.is_cook = not user_dinner.is_cook
                user_dinner.save()
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
            try:
                dinner = Dinner.objects.get(date=input_ud.dinner_date)
            except Dinner.MultipleObjectsReturned as e:
                dinners = Dinner.objects.filter(date=input_ud.dinner_date)
                for dinner in dinners[1:]:
                    dinner.delete()
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
    pagination_class = None

    def get_queryset(self):
        """
        This view should return a list of all dinners
        entered this week.
        """
        return Dinner.objects \
            .filter(date__gte=timezone.now() - timedelta(days=timezone.now().weekday())) \
            .filter(date__lte=timezone.now() + timedelta(days=(7 - timezone.now().weekday()))) \
            .order_by('date')
