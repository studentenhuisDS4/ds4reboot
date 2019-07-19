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
            self.modelType.objects.get(id=value)
        except self.modelType.DoesNotExist:
            raise ValidationError(self._format_error(value, message=self.default_message))
        return value


class ModelAttributeValidator(Validator):
    default_message = "Unique row of {modelType} must exist by ID."
    value_message = "{attribute} is not valid for {modelType}."

    def __init__(self, type, attribute, value=True, error=None):
        if type is None or type(type) == ModelBase:
            raise ValueError(
                'The type must be a django database model.',
            )
        try:
            getattr(type, attribute)
        except AttributeError:
            raise ValueError(
                'That attribute does not exist on this model.',
            )

        self.attribute = attribute
        self.modelType = type
        self.value = value
        self.error = error

        self.default_message = self.default_message.format(modelType=self.modelType)

    def _repr_args(self):
        return 'type={!r}'.format(
            self.modelType
        )

    def _format_error(self, model, message):
        return (self.error or message).format(
            attribute=self.attribute, modelType=model
        )

    def _format_default(self, value, message):
        return (self.error or message).format(
            input=value, modelType=self.modelType
        )

    def __call__(self, value):
        try:
            model = self.modelType.objects.get(id=value)

            if not getattr(model, self.attribute):
                raise ValidationError(self._format_error(model=model, message=self.value_message))

        except self.modelType.DoesNotExist:
            raise ValidationError(self._format_default(value, message=self.default_message))
