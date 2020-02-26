from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from base.models import SoftDeletionModel
from plugins.models import RestAttachment


### This hasnt been implemented in the app or website, nor has it been tested
class KeukenDienst(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deadline = models.DateField(null=True)
    close_time = models.DateTimeField(null=True)
    note = models.CharField(max_length=250)
    done = models.BooleanField(default=False)
    is_leader = models.BooleanField(default=False)


### This has been slightly tested to work with the app (not the site)
class Receipt(models.Model):
    upload_user = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_time = models.DateTimeField(default=timezone.now)

    receipt_cost = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    receipt_title = models.CharField(max_length=100, blank=False, default="Unknown title")
    receipt_description = models.CharField(max_length=500, blank=True)

    accepted = models.NullBooleanField(default=False)
    accepted_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="accepted_user")
    accepted_time = models.DateTimeField(null=True)

    def get_attachments(self):
        object_type = ContentType.objects.get_for_model(self)
        return RestAttachment.objects.filter(content_type__pk=object_type.id, object_id=self.pk)


### This has been slightly tested to work with the app (not the site)
class ReceiptCost(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, null=False)
    affected_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    cost_user = models.DecimalField(max_digits=5, decimal_places=2, null=False)
