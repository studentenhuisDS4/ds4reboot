from django.template.defaulttags import register
import datetime as dt

@register.filter
def disp_date(date):
    return str(date.day).zfill(2) + '/' + str(date.month).zfill(2)

@register.filter
def link_date(date):
    return '/eetlijst/' + str(date.year) + '/' + str(date.month).zfill(2) + '/' + str(date.day).zfill(2) + '/'

@register.filter
def current_date(date):
    for n, d in date.items():
        if d[2] == True:
            return str(d[1]).replace('-','/')