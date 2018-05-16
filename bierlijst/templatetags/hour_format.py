from django.template.defaulttags import register
from user.models import Housemate
from bierlijst.models import Boete


@register.filter
def format_hour(hour):
    h = int(hour)
    if h >= 12:
        if h == 12:
            return str(h) + " PM (noon)"
        else:
            return str(h) + " PM"
    else:
        if h == 12:
            return str(h) + " AM (midnight)"
        else:
            return str(h) + " AM"
