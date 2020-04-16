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
from user.models import SnakeHighScore, SNAKE_NICK_LENGTH

class SnakeHighScoreSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True, validate=[ModelAttributeValidator(type=User, filter='id',
                                                                          attribute='is_active')])
    nickname = fields.Str(required=True, validate=[Length(min=2, max=SNAKE_NICK_LENGTH)])
    score = fields.Int(required=True)
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
            new_highscore = SnakeHighScore.objects.create(**validated_data)
            return new_highscore
        except Exception as e:
            raise ValidationError({'exception': str(e)})