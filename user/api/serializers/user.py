import rest_marshmallow
from django.contrib.auth.models import User
from django.utils import timezone
from marshmallow import fields, validates_schema
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from ds4reboot.api.validators import TextValidator
from user.models import DIET_LENGTH, Housemate

# stupid local fix for bug
rest_marshmallow._schema_kwargs = ('only', 'exclude', 'dump_only', 'load_only', 'context', 'partial')


class PermissionSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    permission_id = fields.Int()


class GroupSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class HousemateSchema(Schema):
    user_id = fields.Int(required=True)
    display_name = fields.Str(required=True, validate=[Length(min=4)])
    diet = fields.Str(validate=[Length(min=4, max=DIET_LENGTH)])
    room_number = fields.Int(required=True)

    movein_date = fields.Date()
    balance = fields.Decimal(max_digits=7, decimal_places=2)
    boetes_total = fields.Int()
    sum_bier = fields.Int()
    sum_rwijn = fields.Decimal(decimal_places=2, max_digits=8)
    sum_wwijn = fields.Decimal(decimal_places=2, max_digits=8)
    total_bier = fields.Int()
    total_rwijn = fields.Decimal(decimal_places=2, max_digits=8)
    total_wwijn = fields.Decimal(decimal_places=2, max_digits=8)


# Necessities only
class UserInfoSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(dump_only=True)

    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=[Length(min=2), TextValidator()])
    last_name = fields.Str(required=True, validate=[Length(min=2), TextValidator()], )
    housemate = fields.Nested(HousemateSchema, exclude=('user_id',), required=True)

    def update(self, instance, validated_data):
        housemate_data = validated_data.pop('housemate')
        housemate = instance.housemate
        for key, value in housemate_data.items():
            setattr(housemate, key, value)
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # first save instance to prevent inconsistent state with SQL errors
        instance.save()
        housemate.save()
        return instance


# Full detail
class UserSchema(UserInfoSchema):
    is_active = fields.Bool(default=True)
    is_staff = fields.Bool(default=False)
    is_superuser = fields.Bool(default=False)
    last_login = fields.DateTime()
    date_joined = fields.DateTime(default=timezone.now())

    # only settable by admin
    username = fields.Str(required=True, validate=[Length(min=4)])
    # TODO move somewhere so it can be adjusted and hashed by users as well
    password = fields.Str(required=True, load_only=True)
    groups = fields.Function(
        lambda user: GroupSchema(user.groups.all(), many=True).data,
        dump_only=True)
    user_permissions = fields.Function(
        lambda user: PermissionSchema(user.user_permissions.all(), many=True).data,
        dump_only=True)

    def create(self, validated_data):
        try:
            housemate_data = validated_data.pop('housemate')
            new_user = User.objects.create_user(**validated_data)
            Housemate.objects.create(**housemate_data, user=new_user)
            return new_user
        except Exception as e:
            raise ValidationError({'exception': str(e)})
