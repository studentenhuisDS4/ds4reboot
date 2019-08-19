from marshmallow import ValidationError, utils
from marshmallow.fields import Nested, Field


class RelatedNested(Nested):

    def _serialize(self, nested_obj, attr, obj, **kwargs):
        # Load up the schema first. This allows a RegistryError to be raised
        # if an invalid schema name was passed
        schema = self.schema
        if nested_obj is None:
            return None
        try:
            return schema.dump(getattr(obj, attr).all(), many=self.many)
        except ValidationError as exc:
            raise ValidationError(exc.messages, valid_data=exc.valid_data) from exc
