from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

class Housemate(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    room_number = models.IntegerField(default=0)
    movein_date = models.DateField(default=timezone.now)

    cell_phone = models.CharField(max_length=50)
    parent_phone = models.CharField(max_length=50)

    balance = models.DecimalField(max_digits=7, decimal_places=4, default=0)

    def __str__(self):
        return self.user.username
