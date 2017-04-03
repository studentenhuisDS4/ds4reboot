from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from django_iban.fields import IBANField
import datetime


# model for thesau reports
class Report(models.Model):

    # basic data
    report_user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=30)
    report_date = models.DateField(auto_now_add=True)
    report_file = models.FileField(upload_to='hr_reports/%Y/%m/%d')
    report_closed = models.BooleanField(default=False)

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


# model for ABN MT940 uploads
class MutationsFile(models.Model):

    # hr data
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True)
    # upload data
    upload_user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # file data
    sta_file = models.FileField(upload_to='bank_uploads/%Y/%m/%d')
    num_mutations = models.IntegerField(default=0)
    num_duplicates = models.IntegerField(default=0)
    applied = models.BooleanField(default=False)
    # finance data
    opening_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    closing_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    opening_date = models.DateField(null=True)
    closing_date = models.DateField(null=True)


# model for parsed ABN MT940 uploads
class MutationsParsed(models.Model):

    # hr data
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    # unparsed original data
    mutation_file = models.ForeignKey(MutationsFile, on_delete=models.CASCADE)
    # parsed mutation
    start_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    end_balance = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    transfer_type = models.CharField(default='D',max_length=1)
    source_IBAN = IBANField(enforce_database_constraint=True, unique=False)
    dest_IBAN = IBANField(enforce_database_constraint=True, unique=False)
    mutation_date = models.DateField(null=True)
    # mutation influence
    applied = models.BooleanField(default=False)
    # label_type = models.
    # label_person = models.





