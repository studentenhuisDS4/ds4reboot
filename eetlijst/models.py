from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from django.db import models


# model for eetlijst date logging
class Dinner(models.Model):
    cook = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    cook_signup_time = models.DateTimeField(null=True)
    close_time = models.DateTimeField(null=True)
    cost_time = models.DateTimeField(null=True)
    eta_time = models.TimeField(null=True)
    date = models.DateField()

    num_eating = models.IntegerField(default=0)
    open = models.BooleanField(default=True)
    cost = models.DecimalField(null=True, max_digits=5, decimal_places=2)


# model for eetlijst signup logging
class UserDinner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    count = models.IntegerField(default=0)
    is_cook = models.BooleanField(default=False)
    split_cost = models.DecimalField(null=True, max_digits=5, decimal_places=2)

    dinner = models.ForeignKey(Dinner, on_delete=models.CASCADE, null=False)
    dinner_date = models.DateField()


# model for transfer logging
class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_from_transfer')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user_to_transfer')
    amount = models.DecimalField(max_digits=4, decimal_places=2)


# model for ho logging
class SplitTransfer(models.Model):
    time = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=4, decimal_places=2)
    note = models.CharField(max_length=20)  # types: ho, transfer, dinner

    # debugging
    total_balance_after = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    total_balance_before = models.DecimalField(default=0, decimal_places=2, max_digits=4, null=True)
    delta_remainder = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    affected_users = ArrayField(models.IntegerField(null=False), default=list)
