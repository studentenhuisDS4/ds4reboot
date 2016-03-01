from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

class Housemate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=12)

    room_number = models.IntegerField(default=0)
    movein_date = models.DateField(default=timezone.now)

    cell_phone = models.CharField(default='06-',max_length=50)
    parent_phone = models.CharField(default='06-', max_length=50)

    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    boetes = models.IntegerField(default=0)

    sum_bier = models.IntegerField(default=0)
    sum_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    sum_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    total_bier = models.IntegerField(default=0)
    total_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    total_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    def __str__(self):
        return self.display_name
