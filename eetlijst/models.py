from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# model for eetlijst date logging
class DateList(models.Model):

    cook = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    signup_time = models.DateTimeField(null=True)
    close_time = models.DateTimeField(null=True)
    date = models.DateField()

    num_eating = models.IntegerField(default=0)
    open = models.BooleanField(default=True)
    cost = models.DecimalField(null=True, max_digits=5, decimal_places=2)


# model for eetlijst signup logging
class UserList(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    list_date = models.DateField()
    list_cook = models.BooleanField(default=False)
    list_count = models.IntegerField(default=0)
    list_cost = models.DecimalField(null=True, max_digits=5, decimal_places=2)


# model for transfer logging
class Transfer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.CharField(max_length=30)
    to_user = models.CharField(max_length=30)

    time = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)


# model for ho logging
class HOLog(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    time = models.DateTimeField(default=timezone.now)
    amount = models.DecimalField(max_digits=4, decimal_places=2)
    note = models.CharField(max_length=20)  # types: ho, transfer, dinner
