from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework import serializers, viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from eetlijst.models import DateList
from user.api.api import SimpleUserSerializer


class DinnerSerializer(serializers.ModelSerializer):
    cook = SimpleUserSerializer()

    class Meta:
        model = DateList
        fields = '__all__'  # Change back to specifics when model is stable
        read_only_fields = ()
        depth = 1


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = DateList.objects.order_by(
        '-date')
    serializer_class = DinnerSerializer


# Week list
class DinnerWeekViewSet(ListModelMixin, GenericViewSet):
    week_ago = datetime.today() - timedelta(days=6)
    queryset = DateList.objects.filter(date__gt=week_ago).order_by(
        'date')
    serializer_class = DinnerSerializer
