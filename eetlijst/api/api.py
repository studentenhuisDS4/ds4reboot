from rest_marshmallow import Schema, fields

from user.api.api import UserInfoSchema


class UserDinnerSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserInfoSchema)

    dinner_date = fields.DateTime()
    is_cook = fields.Bool()
    count = fields.Int()

    # @validates_schema
    # def validate_signup(self, data):
    #     data = Map(data)
    #     errors = {}
    #     if data.turf_count == 0:
    #         errors['turf_count'] = ['Value of turf_count cannot be 0.']
    #     elif data.turf_type == BEER and not is_integer(data.turf_count):
    #         errors['turf_count'] = ['Value of turf_count must be integer for this turf_type.']
    #     elif data.turf_type != BEER and data.turf_count.as_tuple().exponent < -2:
    #         errors['turf_count'] = ['Value of turf_count must have less than or equal to 2 decimal places.']
    #     if errors:
    #         raise ValidationError(errors)
    #     print(type(data.turf_count))
    #
    # def create(self, valid_data, *args, **kwargs):
    #     turf_obj = Turf(**valid_data)
    #     turf_obj.save()
    #     return turf_obj


class DinnerSchema(Schema):
    id = fields.Int()

    date = fields.Date(required=True)
    num_eating = fields.Int()
    userlist_set = fields.Nested(UserDinnerSchema, many=True)
    cook = fields.Nested(UserInfoSchema)
    # cook_id = fields.Int(validate=[UniqueModelValidator(type=User)])
    open = fields.Bool()
    cost = fields.Decimal()

    signup_time = fields.DateTime()
    close_time = fields.DateTime()
    eta_time = fields.DateTime()
