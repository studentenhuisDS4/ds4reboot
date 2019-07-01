from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from bierlijst.api.api import BoeteSerializer, TurfSerializer
from bierlijst.models import Turf, Boete


class TurfViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = Turf.objects.order_by(
        '-turf_time')
    serializer_class = TurfSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=True, methods=['post'])
    def filter(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=False, methods=['post'])
    def turf_beer(self, request):

        # print(self.get_object())
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=True, methods=['post'])
    def turf_wine(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=True, methods=['post'])
    def turf_house(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=True, methods=['post'])
    def turf_crate(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})


class BoeteViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Boete.objects.order_by(
        '-created_time')
    serializer_class = BoeteSerializer

    @action(detail=True, methods=['post'])
    def turf_boete(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})

    @action(detail=True, methods=['post'])
    def create_boete(self, request, pk=None):
        return Response({'status': 'under-construction', 'amount': 0})
