from django.template.defaulttags import register

# custom template tags to check if admin or thesau
@register.filter
def is_admin(user):

    if user.is_superuser:
        return True

    else:
        return False


@register.filter
def is_thesau(user):

    if user.groups.filter(name='thesau').exists():
        return True

    else:
        return False