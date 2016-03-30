from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


# model for thesau reports
class Report(models.Model):

    report_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_time = models.DateTimeField(default=timezone.now)