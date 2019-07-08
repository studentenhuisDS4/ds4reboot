from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from eetlijst.api.api import DinnerSchema, UserDinnerSchema
from eetlijst.models import Dinner, UserDinner


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = Dinner.objects.order_by('-date')
    serializer_class = DinnerSchema


class UserDinnerViewSet(ModelViewSet):
    queryset = UserDinner.objects.order_by('-dinner_date')
    serializer_class = UserDinnerSchema


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
            .filter(date__gte=datetime.now() - timedelta(days=datetime.now().weekday())) \
            .filter(date__lte=datetime.now() + timedelta(days=(7 - datetime.now().weekday()))) \
            .order_by('date')
