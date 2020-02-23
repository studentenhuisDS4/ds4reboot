from django.template.defaulttags import register
import datetime
from django.utils.dateparse import parse_datetime
from django.contrib.humanize.templatetags import humanize

@register.filter
def parse_iso(dateStr):
    date = parse_datetime(dateStr)
    return humanize.naturalday(date)