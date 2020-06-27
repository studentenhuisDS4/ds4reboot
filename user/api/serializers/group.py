from django.contrib.auth.models import Group
from django.utils import timezone
from marshmallow import fields, pre_load, post_dump
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema


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
    id = fields.Int()
    name = fields.Str(required=True, validate=[Length(min=3)])
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

    def update(self, instance, validated_data):
        try:
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except Exception as e:
            raise ValidationError({'exception': str(e)})