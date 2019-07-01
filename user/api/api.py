from django.contrib.auth.models import User
from marshmallow import fields
from rest_framework import serializers
from rest_marshmallow import Schema


class PermissionSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    permission_id = fields.Int()


class GroupSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    group_id = fields.Int()


class HousemateSchema(Schema):
    user_id = fields.Int(required=True)
    movein_date = fields.Date()

    display_name = fields.Str(required=True)
    diet = fields.Str(required=True)

    balance = fields.Decimal(max_digits=7, decimal_places=2)
    boetes_total = fields.Int()
    sum_bier = fields.Int()
    sum_rwijn = fields.Decimal(decimal_places=2, max_digits=8)
    sum_wwijn = fields.Decimal(decimal_places=2, max_digits=8)
    total_bier = fields.Int()
    total_rwijn = fields.Decimal(decimal_places=2, max_digits=8)
    total_wwijn = fields.Decimal(decimal_places=2, max_digits=8)


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)  # 'last_login', 'email', 'date_joined', 'is_staff', 'is_active', 'is_superuser')
        readOnly = '__all__'


# Full detail
class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    is_staff = fields.Bool()
    is_superuser = fields.Bool(default=False)
    is_active = fields.Bool()

    # groups = fields.List(fields.Integer(), required=False)
    # user_permissions = fields.Nested(PermissionSchema, many=True)
    # datelist_set = fields.Nested(DinnerSchema, many=True)

    last_login = fields.DateTime()
    date_joined = fields.DateTime()
    housemate = fields.Nested(HousemateSchema, exclude=('user_id',))


# Necessities only
class UserInfoSchema(Schema):
    id = fields.Int()
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    housemate = fields.Nested(HousemateSchema, exclude=('user_id',))

    # def create(self, validated_data):
    #     return User.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     for key, value in validated_data.items():
    #         setattr(instance, key, value)
    #     instance.save()
    #     return instance
