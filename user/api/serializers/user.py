from django.contrib.auth.models import User
from django.utils import timezone
from marshmallow import fields
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from ds4reboot.api.validators import TextValidator
from user.models import DIET_LENGTH, Housemate


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
    id = fields.Int(load_only=True)

    email = fields.Email(required=True)
    first_name = fields.Str(required=True, validate=[Length(min=2), TextValidator()])
    last_name = fields.Str(required=True, validate=[Length(min=2), TextValidator()], )
    username = fields.Str(required=True, validate=[Length(min=4)])
    housemate = fields.Nested(HousemateSchema, exclude=('user_id',), required=True)

    # def update(self, instance, validated_data):
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance


# Full detail
class UserSchema(UserInfoSchema):
    is_active = fields.Bool(default=True)
    is_staff = fields.Bool(default=False)
    is_superuser = fields.Bool(default=False)
    last_login = fields.DateTime()
    date_joined = fields.DateTime(default=timezone.now())

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
            housemate = Housemate.objects.create(**housemate_data, user=new_user)
            return new_user
        except Exception as e:
            raise ValidationError({'exception': str(e)})
