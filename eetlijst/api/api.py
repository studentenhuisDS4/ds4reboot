from django.contrib.auth.models import User
from django.db.models import Sum
from marshmallow import validates_schema
from marshmallow.validate import Range
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema, fields

from ds4reboot.api.utils import Map
from ds4reboot.api.validators import UniqueModelValidator
from eetlijst.models import UserDinner, Dinner
from user.api.api import UserInfoSchema


class DinnerSchema(Schema):
    id = fields.Int()

    date = fields.Date(required=True)
    num_eating = fields.Int()
    # userdinner_set = RelatedNested(UserDinnerSchema, many=True) # throws Marshmallow error (unknown partial)
    cook = fields.Nested(UserInfoSchema)
    open = fields.Bool()
    cost = fields.Decimal()

    signup_time = fields.DateTime()
    close_time = fields.DateTime()
    eta_time = fields.DateTime()


class UserDinnerSchema(Schema):
    user_id = fields.Int(required=True)
    dinner_date = fields.Date(required=True)

    id = fields.Int(dump_only=True)
    split_cost = fields.Decimal(dump_only=True, max_digits=5, decimal_places=2)
    is_cook = fields.Bool(dump_only=True)
    user = fields.Nested(UserInfoSchema, dump_only=True, validate=[UniqueModelValidator(type=User)])
    dinner = fields.Nested(DinnerSchema, dump_only=True)
    count = fields.Int(dump_only=True, validate=Range(min=0))

    @validates_schema
    def validate_count(self, data):
        data = Map(data)
        errors = {}
        if errors:
            raise ValidationError(errors)

    def create(self, valid_data, *args, **kwargs):
        user_dinner = UserDinner.objects.create(**valid_data)
        return user_dinner, True

    def update(self, instance, validated_data):
        return instance, False
