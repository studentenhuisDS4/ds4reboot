import traceback

from django.contrib.auth.models import User
from marshmallow import fields, post_load, post_dump
from marshmallow.validate import Length
from rest_marshmallow import Schema

# define IO model / serializer here
from ds4reboot.api.utils import log_exception
from ds4reboot.api.validators import ModelAttributeValidator
from organisation.models import Receipt, ReceiptCost
from plugins.models import RestAttachment
from plugins.serializers.attachment import AttachmentsSchema


class ReceiptCostSchema(Schema):
    id = fields.Int(dump_only=True)
    receipt_id = fields.Int(dump_only=True)

    cost_user = fields.Decimal(required=True, max_digits=5, decimal_places=2)
    affected_user_id = fields.Int(required=True, validate=[ModelAttributeValidator(type=User, filter='id')])


class ReceiptSchema(Schema):

    receipt_cost = fields.Decimal(required=True, max_digits=5, decimal_places=2)
    upload_user_id = fields.Int(many=False)

    receipt_attachments = fields.Method("get_attachments", dump_only=True)
    receipt_costs = fields.Function(lambda receipt: ReceiptCostSchema(receipt.receipt_cost_set.all(), many=True).data,
                                    dump_only=True)

    receipt_costs_split = fields.Nested(ReceiptCostSchema, required=True, load_only=True, many=True,
                                        validate=[Length(min=2)])

    def get_attachments(self, obj):
        try:
            attachments = RestAttachment.objects.filter(content_type__model='receipt', object_id=obj.id)
            return AttachmentsSchema(context=self.context['request']).dump(attachments, many=True).data
        except Exception as e:
            return log_exception(e, traceback.format_exc())

    @post_load
    def user_id_loader(self, data):
        data['upload_user_id'] = self.context['request'].user.id

    # close_time, done not exposed
    def create(self, validated_data):
        split_costs = validated_data.pop('receipt_costs_split')
        receipt = Receipt.objects.create(**validated_data)
        for cost in split_costs:
            ReceiptCost.objects.create(**cost, receipt_id=receipt.id)
        return receipt

    def update(self, instance, validated_data):
        # ...
        return validated_data
