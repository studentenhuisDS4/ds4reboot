from django.contrib.auth.models import User, Group
from django.utils import timezone
from marshmallow import fields, validates_schema, pre_load
from marshmallow.validate import Length
from rest_framework.exceptions import ValidationError
from rest_marshmallow import Schema

from marshmallow.validate import NoneOf
from ds4reboot.api.utils import Map
from ds4reboot.api.validators import ModelAttributeValidator
from ds4reboot.api.validators import UniqueModelValidator
from game.models import SnakeHighScore, SNAKE_NICK_LENGTH, MAX_CHAT_MESSAGE_LENGTH

class SnakeChatMessageSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, validate=[UniqueModelValidator(type=User)])
    message = fields.Str(required=True, validate=[Length(min=1, max=MAX_CHAT_MESSAGE_LENGTH)])
    nickname = fields.Str(required=True, validate=[Length(max=SNAKE_NICK_LENGTH)])
    time = fields.DateTime(dump_only=True)

    @pre_load
    def validate_user(self, data, **kwargs):
        if "user_id" in self.context:
            data["user_id"] = self.context["user_id"]
        else:
            raise ValueError("The user_id value was not specified in the Schema context.")
        return data
    
    def create(self, validated_data):
        try:
            new_chatmessage = SnakeChatMessage.objects.create(**validated_data)
            return new_chatmessage
        except Exception as e:
            raise ValidationError({'exception': str(e)})

class SnakeChatClearSchema(Schema):
    remove_all = fields.Bool(required=True)
    remove_user = fields.Int(required=False)

    @pre_load
    def validate_user(self, data, **kwargs):
        if 'remove_all' in data and data["remove_all"] == "false":
            if not "remove_user" in data:
                raise ValidationError({'exception': "The remove_user value was not specified in the Schema data, but 'remove_all' was False."})
        return data