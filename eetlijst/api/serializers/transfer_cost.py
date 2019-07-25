# from marshmallow import Schema, fields
from django.contrib.auth.models import User
from marshmallow import fields, pre_load
from marshmallow.validate import NoneOf, Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from ds4reboot.api.validators import ModelAttributeValidator
from eetlijst.models import Transfer, SplitTransfer
from user.api.api import UserInfoSchema
from user.models import get_active_users, share_cost


class BaseTransferSchema(Schema):
    amount = fields.Decimal(required=True, max_digits=4, decimal_places=2)

    id = fields.Int(dump_only=True)
    time = fields.DateTime(dump_only=True)
    user = fields.Nested(UserInfoSchema, dump_only=True)


class TransferCostSchema(BaseTransferSchema):
    from_user_id = fields.Int(required=True,
                              load_only=True,
                              validate=[NoneOf([1, 2], error="House or Admin cant share costs."),
                                        ModelAttributeValidator(type=User, filter='id',
                                                                attribute='is_active')])
    to_user_id = fields.Int(required=True,
                            load_only=True,
                            validate=[NoneOf([1, 2], error="House or Admin cant share costs."),
                                      ModelAttributeValidator(type=User, filter='id',
                                                              attribute='is_active')])
    user_id = fields.Int(load_only=True)
    from_user = fields.Nested(UserInfoSchema, dump_only=True)
    to_user = fields.Nested(UserInfoSchema, dump_only=True)

    def create(self, data):
        transfer = Transfer(**data)

        from_hm = transfer.from_user.housemate
        from_hm.balance -= transfer.amount

        to_hm = transfer.to_user.housemate
        to_hm.balance += transfer.amount

        transfer.save()
        from_hm.save()
        to_hm.save()
        return transfer

    # validate from_user, to_user not equal and in active users
    @pre_load
    def validate_users(self, data):
        if "user_id" in self.context:
            user_id = self.context["user_id"]
            if data["from_user_id"] == user_id or data["to_user_id"] == user_id:
                data["user_id"] = self.context["user_id"]
            else:
                raise ValidationError("This transfer does not involve the signed-in user and thus is not allowed.")
        else:
            raise ValueError("The user_id value was not specified in the Schema context.")

        if "from_user_id" in data and "to_user_id" in data:
            if data['from_user_id'] == data['to_user_id']:
                raise ValidationError("The transfer can only happen between two different users.")
        return data


class SplitTransferSchema(BaseTransferSchema):
    affected_users = fields.List(required=True,
                                 cls_or_instance=fields.Int(validate=[
                                     ModelAttributeValidator(type=User, filter='id', attribute='is_active')]),
                                 validate=[
                                     Length(min=2, error="Splitting cost requires more than 1 affected user.")])
    user_id = fields.Int(validate=[ModelAttributeValidator(type=User, filter='id', attribute='is_active')])

    delta_remainder = fields.Decimal(max_digits=5, decimal_places=2, dump_only=True)
    total_balance_before = fields.Decimal(max_digits=5, decimal_places=2, dump_only=True)
    total_balance_after = fields.Decimal(max_digits=5, decimal_places=2, dump_only=True)
    note = fields.Str(max_length=20)

    @pre_load
    def provide_affected_users(self, data):
        if not "affected_users" in data:
            data["affected_users"] = [user.id for user in get_active_users()]

    @pre_load
    def validate_users(self, data):
        if "user_id" in self.context:
            data["user_id"] = self.context["user_id"]
        else:
            raise ValueError("The user_id value was not specified in the Schema context.")
        return data

    def create(self, data):
        split_transfer = SplitTransfer(**data)
        ids = split_transfer.affected_users
        housemates = []
        for id in ids:
            housemates.append(User.objects.get(id=id).housemate)

        result = share_cost(housemates=housemates, cost=split_transfer.amount, hm_payback=split_transfer.user.housemate)

        split_transfer.note = "split_cost"
        split_transfer.total_balance_before = result["total_balance_before"]
        split_transfer.total_balance_after = result["total_balance_after"]
        split_transfer.delta_remainder = result["delta_remainder"]
        split_transfer.save()
        return split_transfer
