from django.template.defaulttags import register
import datetime as dt


# display date as DD Month
@register.filter
def disp_date_string(date):
    months = {1: 'januari', 2: 'februari', 3: 'maart', 4: 'april', 5: 'mei', 6: 'juni', 7: 'juli', 8: 'augustus', 9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}
    return str(date.day).zfill(2) + ' ' + months[date.month]

# display the current date as DD/MM
@register.filter
def disp_date(date):
    return str(date.day).zfill(2) + '/' + str(date.month).zfill(2)

# display date as YYYY-MM-DD
@register.filter
def sub_date(date):
    return date.isoformat()

# build date string for url
@register.filter
def link_date(date):
    return '/eetlijst/' + str(date.year) + '/' + str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/'

# check if date is selected
@register.filter
def current_date(date):
    for n, d in date.items():
        if d[2] == True:
            return str(d[1]).replace('-','/')