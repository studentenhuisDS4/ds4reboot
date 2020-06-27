from django.contrib.auth.models import Group
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from ds4reboot.api.utils import IsSuperUser
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
