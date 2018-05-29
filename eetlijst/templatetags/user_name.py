from django.template.defaulttags import register


# display date as DD Month
from user.models import Housemate


@register.simple_tag()
def user2name(user_id):
    try:
        h = Housemate.objects.get(id=user_id)
    except:
        return ""

    return "(Sum: " + str(h) + ")"
