from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Manager
from django.utils import timezone

from base.models import SoftDeletionModel


class KeukenDienst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(null=True)
    close_time = models.DateTimeField(null=True)
    note = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)


class ReceiptManager(Manager):
    def get_attachments(self):
        object_type = ContentType.objects.get_for_model(self)
        return self.filter(content_type__pk=object_type.id, object_id=self.pk)


class Receipt(models.Model):
    objects = ReceiptManager()

    upload_user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(default=timezone.now)

    receipt_cost = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    accepted = models.BooleanField(default=False)
    accepted_user = models.BooleanField(null=True)
    accepted_time = models.BooleanField(null=True)


class ReceiptCost(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=False)
    affected_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    cost_user = models.DecimalField(max_digits=5, decimal_places=2, null=False)
