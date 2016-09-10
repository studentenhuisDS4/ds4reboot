# Fine users with balance below 30 on sunday night

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from user.models import Housemate
from bierlijst.models import Boete


class Command(BaseCommand):
    help = 'Fine users with balance below 30 on sunday night'

    def handle(self, *args, **options):
        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        user_list = Housemate.objects.filter(user__id__in=active_users)

        for h in user_list:
            if h.balance < -30:
                # print 'Boete added for %s' % h.user
                # update housemate object
                h.boetes_open += 1
                h.boetes_total += 1
                h.save()

                 # add entry to boete table
                b = Boete(boete_user=h.user, boete_name=h.display_name, created_by=User.objects.get(username='huis'), boete_count=1, boete_note='Eetlijst saldo te laag')
                b.save()
