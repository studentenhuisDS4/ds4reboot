from django.contrib.auth.models import User
from rest_framework import viewsets, mixins
from rest_framework.permissions import BasePermission
from rest_framework.viewsets import GenericViewSet

from user.api.serializers.user import UserInfoSchema, UserSchema


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class FullProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSchema

    permission_classes = [IsSuperUser, ]


class ProfileViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):
    queryset = User.objects.filter(is_active=True).exclude(username='admin')
    serializer_class = UserInfoSchema
