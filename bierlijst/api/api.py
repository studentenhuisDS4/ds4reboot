from rest_framework import serializers
from rest_marshmallow import Schema, fields

from bierlijst.models import Turf, Boete


class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'
        read_only_field = []


# Action schema
class TurfSchema(Schema):
    amount = fields.Int(required=True, dump_only=True)
    user_id = fields.Int(required=True, dump_only=True)


class BoeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boete
        fields = '__all__'
        read_only_field = []
