from django.conf.global_settings import MEDIA_URL
from django.template.defaulttags import register
from ds4reboot.settings import STATIC_URL


@register.simple_tag(takes_context=True)
def full_static_url(context):
    return get_base(context['request']) + STATIC_URL


@register.simple_tag(takes_context=True)
def full_media_url(context):
    return get_base(context['request']) + MEDIA_URL


@register.simple_tag(takes_context=True)
def audio_url(context, audio_file=''):
    return get_base(context['request']) + STATIC_URL + "audio/" + audio_file


@register.simple_tag(takes_context=True)
def get_params_url(context):
    return "/?" + context['request'].GET.urlencode()


def get_base(request):
    if request.is_secure():
        return "https://" + request.get_host()
    else:
        return "http://" + request.get_host()
