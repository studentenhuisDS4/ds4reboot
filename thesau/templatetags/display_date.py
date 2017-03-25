from django.template.defaulttags import register
import datetime as dt


# display date as DD Month
@register.filter
def disp_date_string(date):
    months = {1: 'januari', 2: 'februari', 3: 'maart', 4: 'april', 5: 'mei', 6: 'juni', 7: 'juli', 8: 'augustus', 9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}
    return str(date.day).zfill(2) + ' ' + months[date.month]