from django.template.defaulttags import register
from eetlijst.models import Dinner, UserDinner
import datetime as dt

# retrieve value from 2D dictionary by tuple index
@register.simple_tag
def get_dict(dict, key_user, key_date):
    tup_userdate = (key_user, key_date)
    if dict.get(tup_userdate , 0 ):
        return dict.get(tup_userdate , 0 )
    else:
        return 0

# check if user is cook
@register.filter
def is_cook(date, id):

    try:
        cook = UserDinner.objects.get(user_id=id, dinner_date=date).is_cook

    except UserDinner.DoesNotExist:
        return 0

    return cook

# get totals for each listed day
@register.filter
def day_total(date):

    try:
        num = Dinner.objects.get(date=date).num_eating

    except Dinner.DoesNotExist:
        return 0

    return int(num)

# get cost if possible
@register.filter
def cost(date, id):

    try:
        cost = UserDinner.objects.get(user_id=id, dinner_date=date).split_cost

    except UserDinner.DoesNotExist:
        cost = 0

    if not cost:
        cost = 0

    return cost

# check if cost is entered
@register.filter
def cost_entered(date):

    try:
        date_entry = Dinner.objects.get(date=date)

        if date_entry.cost:
            entered = True
        else:
            entered = False

    except UserDinner.DoesNotExist:
        entered = False

    return entered
