from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# Create your models here.

class DateList(models.Model):

    list_date = models.DateField(default=timezone.now)

    list_open = models.BooleanField(default=True)
    list_cost = models.DecimalField(max_digits=5, decimal_places=2)


class UserList(models.Model):

    list_user = models.ForeignKey(User, on_delete=models.CASCADE)
    list_timestamp = models.DateTimeField(default=timezone.now)
    list_date = models.DateField()

    list_cook = models.BooleanField(default=False)
    list_count = models.IntegerField()


class Transfer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)

    time = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)


class HOLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    time = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    note = models.CharField(max_length=20)  # types: ho, transfer, dinner
