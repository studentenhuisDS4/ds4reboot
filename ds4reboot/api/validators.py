from django.contrib.auth.models import User
from django.db.models.base import ModelBase
from marshmallow.validate import Validator
from rest_framework.exceptions import ValidationError


class UniqueModelValidator(Validator):
    default_message = "Unique row of {modelType} must exist."

    def __init__(self, type=None, error=None):
        if type is None or type(type) == ModelBase:
            raise ValueError(
                'The type must be a django database model.',
            )

        self.modelType = type
        self.error = error

        self.default_message = self.default_message.format(modelType=self.modelType)

    def _repr_args(self):
        return 'type={!r}'.format(
            self.modelType
        )

    def _format_error(self, value, message):
        return (self.error or message).format(
            input=value, modelType=self.modelType
        )

    def __call__(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise ValidationError(self._format_error(value, message=self.default_message))
        return value
