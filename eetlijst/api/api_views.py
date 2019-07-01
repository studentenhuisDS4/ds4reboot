from datetime import timedelta

from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from eetlijst.api.api import DinnerSchema
from eetlijst.models import DateList


class DinnerViewSet(ListModelMixin, GenericViewSet, RetrieveModelMixin):
    queryset = DateList.objects.order_by('-date')
    serializer_class = DinnerSchema

    @action(detail=True, methods=['post'])
    def signup(self, request, pk=None):
        print(pk)
        return Response({'status': 'under-construction', 'amount': 1})

    @action(detail=True, methods=['post'])
    def cook(self, request, pk=None):
        print(pk)
        return Response({'status': 'under-construction', 'amount': 1})

    @action(detail=True, methods=['post'])
    def close(self, request, pk=None):
        print(pk)
        return Response({'status': 'under-construction', 'amount': 1})

    @action(detail=True, methods=['post'])
    def cost(self, request, pk=None):
        print(pk)
        return Response({'status': 'under-construction', 'cost': 1})


# Week list
class DinnerWeekViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = DinnerSchema
    queryset = DateList.objects.order_by('-date')

    def get_queryset(self):
        """
        This view should return a list of all dinners
        entered this week.
        """
        return DateList.objects \
            .filter(date__gte=datetime.now() - timedelta(days=datetime.now().weekday())) \
            .filter(date__lte=datetime.now() + timedelta(days=(7 - datetime.now().weekday()))) \
            .order_by('date')
