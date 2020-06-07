from django.contrib.auth.models import User, Group
from django.utils import timezone
from marshmallow import fields, validates_schema, pre_load
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from ds4reboot.api.utils import Map
from ds4reboot.api.validators import UniqueModelValidator
from user.models import DIET_LENGTH, Housemate

class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    # members = fields.Nested()

# Full access schema
class GroupAdminSchema(GroupSchema):
    id = fields.Int(required=True, validate=[UniqueModelValidator(type=Group, error="This group does not exist")])

    def create(self, validated_data):
        # try:
        #     housemate_data = validated_data.pop('housemate')
        #     new_user = User.objects.create_user(**validated_data)
        #     Housemate.objects.create(**housemate_data, user=new_user)
        #     return new_user
        # except Exception as e:
        #     raise ValidationError({'exception': str(e)})
        pass
