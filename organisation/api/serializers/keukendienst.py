from pprint import pprint

from marshmallow import fields
from rest_marshmallow import Schema


# define IO model / serializer here
from organisation.models import KeukenDienst


class KeukenDienstSchema(Schema):
    user_id = fields.Int(required=True)
    deadline = fields.Date(required=True)

    id = fields.Int(dump_only=True)
    is_leader = fields.Int(dump_only=True)
    note = fields.Str(max_length=250)

    # close_time, done not exposed
    def create(self, validated_data):
        return KeukenDienst.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # ...
        return validated_data