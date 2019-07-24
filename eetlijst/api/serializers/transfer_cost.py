# from marshmallow import Schema, fields
from marshmallow import fields, validates
from rest_marshmallow import Schema

from ds4reboot.api.validators import ModelAttributeValidator
from eetlijst.models import Transfer
from user.api.api import UserInfoSchema
from user.models import Housemate


class TransferCostSchema(Schema):
    id = fields.Int(dump_only=True)
    time = fields.DateTime(dump_only=True)
    user = fields.Nested(UserInfoSchema, dump_only=True)

    from_user = fields.Str(required=True, validate=[ModelAttributeValidator(type=Housemate, filter='display_name')])
    to_user = fields.Str(required=True, validate=[ModelAttributeValidator(type=Housemate, filter='display_name')])
    amount = fields.Decimal(required=True, max_digits=4, decimal_places=2)

    def create(self, data):
        transfer = Transfer.objects.create(**data)
        return transfer


class SplitCostSchema(Schema):
    id = fields.Int(dump_only=True)
    time = fields.DateTime(dump_only=True)
    user = fields.Nested(UserInfoSchema, dump_only=True)

    from_users = fields.List(fields.Str(validate=[ModelAttributeValidator(type=Housemate, filter='display_name')]),
                             required=True)
    to_user = fields.Str(required=True, validate=[ModelAttributeValidator(type=Housemate, filter='display_name')])
    amount = fields.Decimal(required=True, max_digits=4, decimal_places=2)


class AllCostSchema(Schema):
    id = fields.Int(dump_only=True)
    time = fields.DateTime(dump_only=True)
    user = fields.Nested(UserInfoSchema, dump_only=True)
    
    to_user = fields.Str(required=True, validate=[ModelAttributeValidator(type=Housemate, filter='display_name')])
    amount = fields.Decimal(required=True, max_digits=4, decimal_places=2)
