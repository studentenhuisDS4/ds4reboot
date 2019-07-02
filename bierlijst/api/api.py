from django.contrib.auth.models import User
from marshmallow import validates_schema
from marshmallow.validate import OneOf, Length
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema, fields

from bierlijst.models import Turf, Boete
from ds4reboot.api.utils import Map, is_integer

from ds4reboot.api.validators import UniqueModelValidator
from user.models import Housemate

BEER = 'beer'
RWINE = 'red-wine'
WWINE = 'white-wine'
turf_options = (BEER, RWINE, WWINE)


class TurfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turf
        fields = '__all__'
        read_only_field = []


# Action schema
class TurfSchema(Schema):
    turf_count = fields.Decimal(required=True)
    turf_user_id = fields.Int(required=True, validate=[UniqueModelValidator(type=User)])
    turf_type = fields.Str(required=True,
                           validate=[Length(max=10),
                                     OneOf(turf_options, error=f"The turf type is not of {turf_options}")])
    turf_by = fields.Str(validate=Length(max=30))
    turf_to = fields.Str(validate=Length(max=30))
    turf_note = fields.Str(validate=Length(max=50))

    @validates_schema
    def validate_count(self, data):
        data = Map(data)
        errors = {}
        if data.turf_count == 0:
            errors['turf_count'] = ['Value of turf_count cannot be 0.']
        elif data.turf_type == BEER and not is_integer(data.turf_count):
            errors['turf_count'] = ['Value of turf_count must be integer for this turf_type.']
        elif data.turf_type != BEER and data.turf_count.as_tuple().exponent < -2:
            errors['turf_count'] = ['Value of turf_count must have less than or equal to 2 decimal places.']
        if errors:
            raise ValidationError(errors)
        print(type(data.turf_count))

    def create(self, valid_data, *args, **kwargs):
        turf_obj = Turf(**valid_data)
        turf_obj.save()
        return turf_obj


class BoeteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boete
        fields = '__all__'
        read_only_field = []
