from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django_iban.fields import IBANField


# model for thesau reports
class Report(models.Model):

    # basic data
    report_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=30)
    report_date = models.DateField(default=timezone.now)
    report_path = models.CharField(max_length=50)


# model for report data
class UserReport(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    # store bottle counts
    hr_bier = models.IntegerField(default=0)
    hr_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    hr_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # store boetes
    hr_boetes = models.IntegerField(default=0)

    # eetlijst balance (moving out)
    eetlijst_balance = models.DecimalField(max_digits=5, decimal_places=2, default=0)


# model for HR boetes
class BoetesReport(models.Model):

    type = models.CharField(max_length=30)
    boete_count = models.IntegerField(default=0)


# model for parsed ABN MT940 uploads
class AbnMutationsParsed(models.Model):
    report_id = models.IntegerField(default=None)
    start_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    end_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    source_IBAN = IBANField(enforce_database_constraint=True, unique=False)
    report_date = models.DateField(null=True)


# model for ABN MT940 uploads
class ABNMutations(models.Model):

    # basic data
    report_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_id = models.IntegerField(default=None)
    report_date = models.DateField(default=timezone.now)
    report_path = models.CharField(default=None, max_length=50)



