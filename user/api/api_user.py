from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from ds4admin.utils import check_dinners_housemate
from ds4reboot.api.utils import illegal_action, IsSuperUser, EmptySchema, log_exception, \
    success_action
from eetlijst.api.serializers.transfer_cost import SplitTransferSchema
from user.api.actions import moveout_user
from user.api.serializers.user import UserSchema, UserFullSchema, GroupSchema
from user.models import get_active_users


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = get_active_users()
    serializer_class = UserSchema
    filter_fields = '__all__'


class HouseViewSet(mixins.RetrieveModelMixin,
                   GenericViewSet):
    queryset = User.objects.filter(username__in=['huis'])
    serializer_class = UserSchema


class UserFullViewSet(viewsets.ModelViewSet):
    queryset = User.objects.exclude(username__in=['admin', 'huis'])
    serializer_class = UserFullSchema

    permission_classes = [IsSuperUser, ]
    filter_fields = '__all__'


class UserActionViewSet(viewsets.GenericViewSet):
    queryset = User.objects.exclude(username__in=['admin', 'huis'])
    serializer_class = EmptySchema

    permission_classes = [IsSuperUser, ]

    @action(detail=True, methods=['DELETE'])
    def moveout(self, request, pk=None):
        removed_user = self.get_object()
        hm = removed_user.housemate
        if removed_user.id == request.user.id:
            return illegal_action("Cant remove yourself (superuser must exist).")
        if hm.moveout_set:
            return illegal_action("This user was already moved out.")

        unpayed_dinners = check_dinners_housemate(request, hm)
        safe_to_remove = True
        unsafe_string = ""
        for dinner in unpayed_dinners:
            if dinner.cook.is_active:
                safe_to_remove = False
                unsafe_string += f"(Cook: {dinner.cook.housemate.display_name}, date: {str(dinner.date)}), "
        if not safe_to_remove:
            return illegal_action(
                f"You can\'t deactivate {hm.display_name}. Please check unsafe dinners: {unsafe_string}")

        removed_user.refresh_from_db()
        try:
            user, transfer = moveout_user(request, removed_user)
            return success_action({
                'user': UserFullSchema(user).data,
                'transfer': SplitTransferSchema(transfer).data
            })
        except Exception as e:
            return log_exception(e)

    @action(detail=True, methods=['POST'])
    def toggle_activation(self, request, pk=None):
        user = self.get_object()
        hm = user.housemate
        user.is_active = not user.is_active
        if user.id == request.user.id:
            return illegal_action("Cant deactivate yourself (superuser must exist).")
        if hm.moveout_set:
            return illegal_action(
                f"Cant (de)activate already moved out user {user.housemate.display_name}. "
                "This action excludes the user from shared costs for a limited period, but keeps the original balance.")

        if hm.sublet_date:
            hm.sublet_date = None
        else:
            hm.sublet_date = timezone.now()
        user.save()
        hm.save()
        user.refresh_from_db()

        return success_action({
            'user': UserFullSchema(user).data,
            'activation': user.is_active
        })

    @action(detail=True, methods=['POST'])
    def set_groups(self, request, pk=None):
        user = self.get_object()
        hm = user.housemate
        if hm.moveout_set:
            return illegal_action(f"Not allowed to set groups for moved out user {user.housemate.display_name}.")

        serializer = GroupSchema(data=request.data, many=True)
        if serializer.is_valid():
            user.groups.clear()
            for group in serializer.data:
                user.groups.add(group['id'])
            user.save()
        else:
            return illegal_action(serializer.errors)

        user.save()
        hm.save()
        user.refresh_from_db()

        return success_action({
            'user': UserFullSchema(user).data,
        })

    @action(detail=True, methods=['POST'])
    def toggle_admin(self, request, pk=None):
        user = self.get_object()
        hm = user.housemate

        if hm.moveout_set:
            return illegal_action(f"Not allowed to make moved out user {user.housemate.display_name} admin.")
        if not user.is_active and not user.is_superuser:
            return illegal_action(f"Cant set inactive user {user.housemate.display_name} to admin.")
        if user.id == request.user.id and user.is_superuser:
            return illegal_action("Cant remove admin flag for yourself (superuser must exist).")
        user.is_superuser = not user.is_superuser
        user.is_staff = user.is_superuser
        user.save()

        user.save()
        hm.save()
        user.refresh_from_db()

        return success_action({
            'user': UserFullSchema(user).data,
        })
