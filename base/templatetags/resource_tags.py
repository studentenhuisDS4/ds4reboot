from django.conf.global_settings import MEDIA_URL
from django.template.defaulttags import register
from ds4reboot.settings import STATIC_URL


@register.simple_tag(takes_context=True)
def full_static_url(context):
    return "http://" + context['request'].get_host() + STATIC_URL


@register.simple_tag(takes_context=True)
def full_media_url(context):
    return "http://" + context['request'].get_host() + MEDIA_URL


@register.simple_tag(takes_context=True)
def audio_url(context, audio_file):
    return "http://" + context['request'].get_host() + STATIC_URL + "audio/" + audio_file


@register.simple_tag(takes_context=True)
def get_params_url(context):
    return "/?" + context['request'].GET.urlencode()

