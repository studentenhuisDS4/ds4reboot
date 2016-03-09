from django.template.defaulttags import register
from user.models import Housemate
from bierlijst.models import Boete

@register.filter
def can_del(boete_id, user_id):

    if Boete.objects.get(pk=boete_id).boete_count <= Housemate.objects.get(user_id=user_id).boetes_open:
        return True

    else:
        return False