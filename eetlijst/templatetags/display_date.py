from django.template.defaulttags import register
import datetime as dt


# display the current date as MM/DD
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