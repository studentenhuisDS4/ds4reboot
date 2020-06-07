from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.utils.datetime_safe import datetime
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import illegal_action, IsSuperUser, EmptySchema, log_exception, \
    success_action
from user.api.serializers.group import GroupSchema


class GroupViewSet(mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSchema
    filter_fields = '__all__'


class GroupAdminViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSchema

    permission_classes = [IsSuperUser, ]
    filter_fields = '__all__'
