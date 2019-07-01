from rest_marshmallow import Schema, fields

from user.api.api import UserInfoSchema


class UserDinnerSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserInfoSchema)

    list_date = fields.DateTime()
    list_cook = fields.Bool()
    list_count = fields.Int()


class DinnerSchema(Schema):
    id = fields.Int()

    date = fields.Date(required=True)
    num_eating = fields.Int()
    userlist_set = fields.Nested(UserDinnerSchema, many=True, dump_only=True)
    cook = fields.Nested(UserInfoSchema)
    open = fields.Bool()
    cost = fields.Decimal()

    signup_time = fields.DateTime()
    close_time = fields.DateTime()
    eta_time = fields.DateTime()
