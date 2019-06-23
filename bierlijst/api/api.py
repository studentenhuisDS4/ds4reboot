from rest_framework import serializers
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from bierlijst.models import Turf, Boete


class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'
        read_only_field = []


class BoeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boete
        fields = '__all__'
        read_only_field = []


class TurfViewSet(ListModelMixin,
                  RetrieveModelMixin,
                  GenericViewSet):
    queryset = Turf.objects.order_by(
        '-turf_time')
    serializer_class = TurfSerializer


class BoeteViewSet(ListModelMixin,
                   RetrieveModelMixin,
                   GenericViewSet):
    queryset = Boete.objects.order_by(
        '-created_time')
    serializer_class = BoeteSerializer


class TurfAPIView(APIView):
    def post(self):
        # turf beer
        print('WIP')
