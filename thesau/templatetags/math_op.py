from django.template.defaulttags import register
from decimal import Decimal

@register.filter
def subtract(value, arg):
    ans = arg - value
    if ans > Decimal(0.00):
        return '<span class="uk-text-success"> ' + str(ans) + ' </span>'
    else:
        return '<span class="uk-text-danger"> ' + str(ans) + ' </span>'