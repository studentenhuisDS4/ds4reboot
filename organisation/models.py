from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class KeukenDienst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(null=True)
    close_time = models.DateTimeField(null=True)
    note = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)
