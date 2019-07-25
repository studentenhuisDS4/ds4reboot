from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# model for housemates (linked to auth user)
from base.models import SoftDeletionModel


def get_active_users():
    return User.objects.filter(is_active=True).exclude(username__in=['huis', 'admin'])


class Housemate(SoftDeletionModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=12)

    # logistics
    room_number = models.IntegerField(null=True)
    movein_date = models.DateField(default=timezone.now)
    moveout_date = models.DateField(null=True)

    # flag user for moveout (null=normal, false=ready for deletion, true=deleted)
    moveout_set = models.NullBooleanField()

    # phone numbers
    cell_phone = models.CharField(default='06', max_length=50)
    parent_phone = models.CharField(max_length=50, blank=True)

    # eetlijst related values
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    diet = models.CharField(max_length=100, blank=True)

    # store boete counts and status
    boetes_open = models.IntegerField(default=0)
    boetes_geturfd_rwijn = models.IntegerField(default=0)
    boetes_geturfd_wwijn = models.IntegerField(default=0)
    boetes_total = models.IntegerField(default=0)

    # store bottle counts since last HR
    sum_bier = models.IntegerField(default=0)
    sum_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    sum_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # store total bottle counts
    total_bier = models.IntegerField(default=0)
    total_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    total_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # sum wine columns
    def get_sum_wijn(self):
        return self.sum_wwijn + self.sum_rwijn

    def get_total_wijn(self):
        return self.total_wwijn + self.total_rwijn

    sum_wijn = property(get_sum_wijn)
    total_wijn = property(get_total_wijn)

    def __str__(self):
        return self.display_name
