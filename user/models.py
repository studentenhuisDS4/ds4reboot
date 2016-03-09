from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# model for housemates (linked to auth user)
class Housemate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=12)

    room_number = models.IntegerField(default=0)
    movein_date = models.DateField(default=timezone.now)

    cell_phone = models.CharField(default='06-',max_length=50)
    parent_phone = models.CharField(default='06-', max_length=50)

    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    boetes_open = models.IntegerField(default=0)
    boetes_turfed = models.IntegerField(default=0)
    boetes_total = models.IntegerField(default=0)

    sum_bier = models.IntegerField(default=0)
    sum_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    sum_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

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
