from django.db.models.base import ModelBase
from marshmallow import ValidationError
from marshmallow.validate import Validator


class UniqueModelValidator(Validator):
    """ ModelAttributeValidator does more and better """
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
    """ ModelAttributeValidator checks unique filter result and optional checks for attribute not None. """
    default_message = "Unique row of {modelType} must exist by {filter}."
    filter_message = "{filter} filter did not give a {modelType} model."
    attr_message = "{attribute} is not valid for {modelType}."

    # Attribute is optional
    def __init__(self, type, filter, attribute=None, error=None):
        if type is None or type(type) == ModelBase:
            raise ValueError(
                'The type must be a django database model.',
            )
        try:
            getattr(type, filter)
        except AttributeError:
            raise ValueError(
                'That columns does not exist on this model.',
            )

        if attribute:
            try:
                getattr(type, attribute)
            except AttributeError:
                raise ValueError(
                    'That attribute does not exist on this model.',
                )

        self.filter = filter
        self.attribute = attribute
        self.modelType = type
        self.error = error

        self.default_message = self.default_message.format(modelType=self.modelType,
                                                           filter=self.filter)

    def _repr_args(self):
        return 'type={!r}'.format(
            self.modelType
        )

    def _format_error(self, model, message):
        return (self.error or message).format(
            modelType=model, filter=self.filter, attribute=self.attribute,
        )

    def _format_default(self, value, message):
        return (self.error or message).format(
            input=value, modelType=self.modelType
        )

    def __call__(self, value):
        try:
            filter = {self.filter: value}
            model = self.modelType.objects.get(**filter)
            if not model:
                raise ValidationError(self._format_error(model=model, message=self.filter_message))
            if self.attribute and not getattr(model, self.attribute):
                raise ValidationError(self._format_error(model=model, message=self.attr_message))
        except self.modelType.DoesNotExist:
            raise ValidationError(self._format_default(value, message=self.default_message))


class TextValidator(Validator):
    """ ModelAttributeValidator checks unique filter result and optional checks for attribute not None. """
    default_message = "Value contains illegal symbols. Only text is allowed."

    # Attribute is optional
    def __init__(self, error=None):
        self.error = error

    def _repr_args(self):
        return 'error={!r}'.format(
            self.error
        )

    def _format_default(self, message):
        return self.error or message

    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError(self._format_default(self.default_message))
