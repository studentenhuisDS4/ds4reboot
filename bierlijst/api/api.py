from rest_framework import serializers

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