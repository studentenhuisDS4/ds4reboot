from django.contrib.auth.models import User
from marshmallow import validates_schema
from marshmallow.validate import Range, NoneOf
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema, fields

from ds4reboot.api.utils import Map
from ds4reboot.api.validators import ModelAttributeValidator
from eetlijst.models import UserDinner, Dinner
from user.api.serializers.user import UserSchema


class UserDinnerSchema(Schema):
    # none of house/admin
    user_id = fields.Int(required=True, validate=[NoneOf([1, 2], error="House or Admin cant join dinner."),
                                                  ModelAttributeValidator(type=User, filter='id',
                                                                          attribute='is_active')])
    dinner_date = fields.Date(required=True)

    # Tighten the strictness on data validation
    id = fields.Int(dump_only=True)
    split_cost = fields.Decimal(dump_only=True, max_digits=5, decimal_places=2)
    is_cook = fields.Bool(dump_only=True)
    user = fields.Nested(UserSchema, dump_only=True)
    count = fields.Int(dump_only=True, validate=Range(min=0))

    @validates_schema
    def validate_count(self, data, **kwargs):
        data = Map(data)
        errors = {}
        if errors:
            raise ValidationError(errors)

    def create(self, valid_data, *args, **kwargs):
        map_data = Map(valid_data)
        try:
            dinner, _ = Dinner.objects.get_or_create(date=map_data.dinner_date)
        except Dinner.MultipleObjectsReturned as e:
            dinners = Dinner.objects.filter(date=map_data.dinner_date)
            for dinner in dinners[1:]:
                dinner.delete()
            dinner = Dinner.objects.get(date=map_data.dinner_date)
        valid_data.update({'dinner_id': dinner.id})
        try:
            user_dinner, created = UserDinner.objects.get_or_create(**valid_data)
        except UserDinner.MultipleObjectsReturned as e:
            uds = UserDinner.objects.filter(user_id=valid_data['user_id'], dinner_date=valid_data['dinner_date'])
            for ud in uds[1:]:
                ud.delete()
            user_dinner, created = UserDinner.objects.get_or_create(**valid_data)
        return user_dinner, created

    # Our update is not done here, and somehow currently not working anyway (bug?)
    def update(self, instance, validated_data):
        return instance, False


class DinnerSchema(Schema):
    # print(requirements)
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    num_eating = fields.Int(dump_only=True)
    userdinners = fields.Function(lambda dinner: UserDinnerSchema(dinner.userdinner_set.all(), many=True).data,
                                  dump_only=True)
    cook = fields.Nested(UserSchema, dump_only=True)
    open = fields.Bool(dump_only=True)
    cook_signup_time = fields.DateTime(dump_only=True)
    close_time = fields.DateTime(dump_only=True)
    cost_time = fields.DateTime(dump_only=True)

    cost = fields.Decimal(required=True, validate=[
        Range(min=1, error="The cost must be bigger than 1 euro. What are you thinking?", )])
    eta_time = fields.Time(required=True)
