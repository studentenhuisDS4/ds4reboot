from django.contrib.auth.models import Group, User
from django.utils import timezone
from marshmallow import fields, pre_load, post_dump, EXCLUDE
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

INDEX_KEY = 'id'
MEMBERS_KEY = 'members'


class GroupHousemateSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    display_name = fields.Str(dump_only=True)
    movein_date = fields.Date(default=timezone.now())
    moveout_set = fields.Boolean(default=False, dump_only=True)
    moveout_date = fields.Date(dump_only=True)


class GroupUserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int(required=True)
    username = fields.Str(dump_only=True)
    is_active = fields.Bool(dump_only=True)
    is_staff = fields.Bool(dump_only=False)
    is_superuser = fields.Bool(dump_only=False)
    first_name = fields.Str(dump_only=True)
    last_name = fields.Str(dump_only=True)
    housemate = fields.Nested(
        GroupHousemateSchema, dump_only=True)


class GroupSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    id = fields.Int()
    name = fields.Str(required=True, validate=[Length(min=3)])
    members = fields.Nested(GroupUserSchema,
                            many=True,
                            data_key=MEMBERS_KEY,
                            validate=[Length(min=0)],
                            required=True)
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
            self._add_group_members(new_group, validated_data)
            return new_group
        except Exception as e:
            raise ValidationError({'exception': str(e)})

    def update(self, instance, validated_data):
        try:
            # Save user_set of group
            self._add_group_members(instance, validated_data)
            # Now save attributes
            for key, value in validated_data.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except Exception as e:
            raise ValidationError({'exception': str(e)})

    def _add_group_members(self, instance, validated_data):
        if MEMBERS_KEY in validated_data:
            # Delete members from validated_data
            members_list = validated_data.pop(MEMBERS_KEY)
            validated_user_ids = list()
            if len(members_list) == 0:
                raise ValidationError('Groups without members ... are just sad.')
            for member in members_list:
                if INDEX_KEY not in member:
                    raise ValidationError(member.id, f'{INDEX_KEY} field missing')
                elif not str(member[INDEX_KEY]).isnumeric():
                    raise ValidationError(member.id, f'{INDEX_KEY} is not numeric')
                validated_user_ids.append(member[INDEX_KEY])

            # Add list of users to group user_set
            filtered_users = User.objects \
                .filter(pk__in=validated_user_ids)
            instance.user_set.clear()
            for user in filtered_users:
                instance.user_set.add(user)
