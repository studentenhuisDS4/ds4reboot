from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.apps import apps
from marshmallow import fields, validates_schema, pre_load, pre_dump, post_dump
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from ds4reboot.api.utils import Map
from ds4reboot.api.validators import UniqueModelValidator
from user.models import DIET_LENGTH, Housemate


class GroupHousemateSchema(Schema):
    display_name = fields.Str(dump_only=True)
    movein_date = fields.Date(default=timezone.now())
    moveout_set = fields.Boolean(default=False, dump_only=True)
    moveout_date = fields.Date(dump_only=True)


class GroupUserSchema(Schema):
    id = fields.Int(required=True)
    username = fields.Str(dump_only=True)
    is_staff = fields.Bool(dump_only=False)
    is_superuser = fields.Bool(dump_only=False)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    housemate = fields.Nested(
        GroupHousemateSchema, dump_only=True)


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=[Length(min=4)])
    members = fields.Nested(GroupUserSchema, many=True)
    _members = fields.Function(
        lambda group: GroupUserSchema(
            group.user_set.all(), many=True).data,
        dump_only=True)

    @pre_load
    def process_group_ids(self, in_data, **kwargs):
        if hasattr(in_data, 'name'):
            in_data['name'] = in_data['name'].strip()
        return in_data

    @post_dump
    def dump_groups(self, data, **kwargs):
        data['members'] = data['_members']
        data.pop('_members')
        return data

    def create(self, validated_data):
        try:
            new_group = Group.objects.create(name=validated_data['name'])
            return new_group
        except Exception as e:
            raise ValidationError({'exception': str(e)})
