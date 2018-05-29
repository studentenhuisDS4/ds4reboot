from django.template.defaulttags import register
import datetime


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


@register.filter
def format_month(int_month):
    if int_month:
        m = datetime.date(1900, int(int_month), 1).strftime('%B')
        return m
    else:
        return ''
