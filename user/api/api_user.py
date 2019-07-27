from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from ds4admin.utils import check_dinners_housemate
from ds4reboot.api.utils import illegal_action, IsSuperUser, EmptySchema, log_exception, \
    success_action
from eetlijst.api.serializers.transfer_cost import SplitTransferSchema
from user.api.actions import moveout_user
from user.api.serializers.user import UserSchema, UserFullSchema
from user.models import get_active_users


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = get_active_users()
    serializer_class = UserSchema


class UserFullViewSet(viewsets.ModelViewSet):
    queryset = get_active_users()
    serializer_class = UserFullSchema

    permission_classes = [IsSuperUser, ]


class UserActionViewSet(viewsets.GenericViewSet):
    queryset = User.objects.exclude(username__in=['admin', 'huis'])
    serializer_class = EmptySchema

    permission_classes = [IsSuperUser, ]

    @action(detail=True, methods=['DELETE'])
    def moveout(self, request, pk=None):
        removed_user = self.get_object()
        hm = removed_user.housemate
        if removed_user.id == request.user.id:
            return illegal_action("Cant deactivate yourself (superuser must exist).")
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
