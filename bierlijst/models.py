from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

class Turf(models.Model):

    turf_user = models.ForeignKey(User, on_delete=models.CASCADE)

    turf_time = models.DateTimeField(default=timezone.now)

    turf_count = models.DecimalField(default=1, decimal_places=2, max_digits=4)
    turf_type = models.CharField(max_length=10)



class Boete(models.Model):

    boete_user = models.ForeignKey(User, on_delete=models.CASCADE)

    time_opened = models.DateTimeField(default=timezone.now)
    time_closed = models.DateTimeField()

    boete_open = models.BooleanField(default=True)
    boete_note = models.CharField(max_length=50)