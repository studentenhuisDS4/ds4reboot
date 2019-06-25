from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# model for thesau reports
from ds4reboot.settings import HR_REPORTS_FOLDER


class Report(models.Model):
    # basic data
    report_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=30)
    report_date = models.DateField(default=timezone.now)
    report_file = models.FileField(upload_to=HR_REPORTS_FOLDER)


# model for report data
class UserReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    # store bottle counts
    hr_bier = models.IntegerField(default=0)
    hr_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    hr_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # store boetes
    hr_boete_rwijn = models.IntegerField(default=0)
    hr_boete_wwijn = models.IntegerField(default=0)

    # eetlijst balance (moving out)
    eetlijst_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0)


# model for HR boetes
class BoetesReport(models.Model):
    type = models.CharField(max_length=30)
    boete_count = models.IntegerField(default=0)
