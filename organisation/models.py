from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from base.models import SoftDeletionModel
from ds4reboot.settings import RECEIPTS_FOLDER


class KeukenDienst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(null=True)
    close_time = models.DateTimeField(null=True)
    note = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)


class Receipt(SoftDeletionModel):
    upload_user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(default=timezone.now)

    receipt_file = models.ImageField(upload_to=RECEIPTS_FOLDER, )
    receipt_cost = models.DecimalField(max_digits=5, decimal_places=2)
    # receipt_target_user

    accepted = models.BooleanField(default=False)
    accepted_user = models.BooleanField(default=False)
    accepted_time = models.BooleanField(default=False)