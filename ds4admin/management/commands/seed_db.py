# Fine users with balance below 30 on sunday night

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from user.models import Housemate
from bierlijst.models import Boete

from ds4reboot.secret_settings import *

class Command(BaseCommand):
    help = 'Seed database in DEBUG scenario' #asd

    def handle(self, *args, **options):
        if not DEBUG:
            exit("Init db is not possible in Production scenario. Exiting...")
    
        # Call migrate
        from django.core.management import call_command
        call_command('migrate')

        default_user = User.objects.get(username='default')
        if not default_user:
            print('Creating \'default\' superuser ')
            call_command('createsuperuser', '--noinput', '--username','default', '--password','default', '--username','admin@ds4.nl')
        else:
            print('Already exists: \'default\' superuser ')
        if default_user and not hasattr(User.objects.get(username='default'), 'housemate'):
            print('Creating user \'default\' Housemate metadata entry')
            default_user.housemate = Housemate.objects.create(user_id=default_user.id, diet="",
                                            cell_phone="06-", parent_phone="",
                                            display_name="Default",
                                            room_number=None)
            default_user.housemate.save()
            default_user.save()
        else:
            print('Already exists: \'default.housemate\' metadata ')

