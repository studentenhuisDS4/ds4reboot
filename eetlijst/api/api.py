import traceback
from pprint import pprint

from marshmallow import post_load, pre_load
from marshmallow.validate import Range
from rest_marshmallow import Schema, fields

from ds4reboot.api.utils import log_exception
from ds4reboot.secret_settings import DEBUG
from eetlijst.models import UserDinner, Dinner
from user.api.api import UserInfoSchema


class DinnerSchema(Schema):
    id = fields.Int()

    date = fields.Date(required=True)
    num_eating = fields.Int()
    # userdinner_set = RelatedNested(UserDinnerSchema, many=True) # throws Marshmallow error (unknown partial)
    cook = fields.Nested(UserInfoSchema)
    open = fields.Bool()
    cost = fields.Decimal()

    signup_time = fields.DateTime()
    close_time = fields.DateTime()
    eta_time = fields.DateTime()


class UserDinnerSchema(Schema):
    id = fields.Int()
    user = fields.Nested(UserInfoSchema, dump_only=True)
    user_id = fields.Int(required=True, load_only=True)
    is_cook = fields.Bool()
    count = fields.Int(validate=Range(min=0))
    split_cost = fields.Decimal(max_digits=5, decimal_places=2, dump_only=True, allow_none=True)

    dinner = fields.Nested(DinnerSchema, dump_only=True)
    dinner_date = fields.Date(required=True)

    def create(self, valid_data, *args, **kwargs):
        userdinner_obj, created_at = UserDinner.objects.get_or_create(**valid_data)
        dinner, created_at = Dinner.objects.get_or_create(date=userdinner_obj.dinner_date)

        dinner.num_eating = len(UserDinner.objects.filter(dinner_date=userdinner_obj.dinner_date))
        userdinner_obj.dinner = dinner

        dinner.save()
        userdinner_obj.save()
        return userdinner_obj

    def update(self, instance, valid_data):
        try:
            userdinner_queried = UserDinner.objects.filter(id=instance.id)
            userdinner_queried.update(**valid_data)

            userdinner = userdinner_queried[0]

            if DEBUG:
                print(len(UserDinner.objects.filter(dinner_date=userdinner.dinner_date)))
                print(UserDinner.objects.filter(dinner_date=userdinner.dinner_date))
            userdinner.dinner.num_eating = len(UserDinner.objects.filter(dinner_date=userdinner.dinner_date))
            userdinner.dinner.save()

            if not userdinner.count:
                userdinner.delete()
            if not userdinner.dinner.num_eating:
                userdinner.dinner.delete()
            return instance
        except Exception as e:
            pprint(traceback.format_exc())
            raise log_exception(e)
