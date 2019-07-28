from pprint import pprint

from marshmallow import fields
from rest_marshmallow import Schema


# define IO model / serializer here
from organisation.models import KeukenDienst
from user.api.serializers.user import UserSchema


class ReceiptSchema(Schema):
    receipt_cost = fields.Decimal(required=True, max_digits=5, decimal_places=2)
    upload_user = fields.Nested(UserSchema, many=False)

    # close_time, done not exposed
    def create(self, validated_data):
        return None # KeukenDienst.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # ...
        return validated_data