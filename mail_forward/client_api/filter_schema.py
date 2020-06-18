from marshmallow import fields
from marshmallow.validate import Length
from rest_marshmallow import Schema

MAX_RULENAME_LENGTH = 100


class FlagSchema(Schema):
    pass


class TestSchema(Schema):
    # Vital to be present and 'true', but functionally useless
    id = fields.Str(required=True, default="true")


class ActionCmdSchema(Schema):
    id = fields.Str(required=True, default='redirect')  # certainly not required, but must exist. Can be 'redirect' (singleton).
    to = fields.Str(required=True)


class MijndomeinMailFilterSchema(Schema):
    id = fields.Int()
    position = fields.Int(required=False)
    # Name not required, but enforced here.
    rulename = fields.Str(required=True,
                          validate=[Length(min=2, max=MAX_RULENAME_LENGTH)])
    active = fields.Bool(required=True)
    actioncmds = fields.Nested(ActionCmdSchema, many=True, default=[])
    test = fields.Nested(TestSchema, required=True, many=False, default={'id': 'true'})
    flags = fields.Nested(FlagSchema, many=True)
