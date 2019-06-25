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
    queryset = DateList.objects \
        .filter(date__gte=datetime.now() - timedelta(days=datetime.now().weekday())) \
        .filter(date__lte=datetime.now() + timedelta(days=(7 - datetime.now().weekday()))) \
        .order_by('date')
    serializer_class = DinnerSerializer
