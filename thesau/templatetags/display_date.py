from django.template.defaulttags import register


# display date as DD Month
@register.filter
def disp_date_string(date):
    months = {1: 'jan.', 2: 'feb.', 3: 'mar.', 4: 'apr.', 5: 'mei', 6: 'juni', 7: 'juli', 8: 'aug.', 9: 'sept.', 10: 'okt.', 11: 'nov.', 12: 'dec.'}
    if date is not None:
        return str(date.day).zfill(2) + ' ' + months[date.month]
    else:
        return '-'