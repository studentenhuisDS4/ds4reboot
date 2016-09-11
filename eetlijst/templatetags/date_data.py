from django.template.defaulttags import register
from eetlijst.models import DateList, UserList
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
        cook = UserList.objects.get(user_id=id, list_date=date).list_cook

    except UserList.DoesNotExist:
        return 0

    return cook

# get totals for each listed day
@register.filter
def day_total(date):

    try:
        num = DateList.objects.get(date=date).num_eating

    except DateList.DoesNotExist:
        return 0

    return int(num)

# get cost if possible
@register.filter
def cost(date, id):

    try:
        cost = UserList.objects.get(user_id=id, list_date=date).list_cost

    except UserList.DoesNotExist:
        cost = 0

    if not cost:
        cost = 0

    return cost

# check if cost is entered
@register.filter
def cost_entered(date):

    try:
        date_entry = DateList.objects.get(date=date)

        if date_entry.cost:
            entered = True
        else:
            entered = False

    except UserList.DoesNotExist:
        entered = False

    return entered
