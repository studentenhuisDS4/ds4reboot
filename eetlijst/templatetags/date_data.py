from django.template.defaulttags import register
from eetlijst.models import DateList, UserList
import datetime as dt

# check if user is cook
@register.filter
def is_cook(date, id):

    try:
        cook = UserList.objects.get(user_id=id, list_date=date).list_cook

    except UserList.DoesNotExist:
        return 0

    return cook

# check if user is eating with
@register.filter
def eating_with(date, id):
    try:
        eating = UserList.objects.get(user_id=id, list_date=date).list_count

    except UserList.DoesNotExist:
        return 0

    return eating

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
