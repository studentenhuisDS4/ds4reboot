from django.contrib.auth.models import User
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from user.api.api import SimpleUserSerializer


class ProfileViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = SimpleUserSerializer

    # def get_serializer_class(self):
    #     lookup = self.lookup_url_kwarg or self.lookup_field
    #     if lookup and lookup in self.kwargs:
    #         # get detailed endpoint value from url e.g, "/users/2/" => 2
    #         user_pk = self.kwargs[lookup]
    #         lookup_user = User.objects.filter(pk=user_pk).first()
    #         # if current user is looking at the details
    #         if self.request.user == lookup_user:
    #             return self.serializer_detail_class
    #
    #         # if current user is sys admin of the requested user's company
    #         if (self.request.user.system_role == SystemUserRole.SYS_ADMIN and
    #                 self.request.user.company == lookup_user.company):
    #             return self.serializer_detail_class
    #
    #         return super().get_serializer_class()
    #     else:
    #         return super().get_serializer_class()
