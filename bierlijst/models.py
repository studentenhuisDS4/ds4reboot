from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models import Sum


# model to account for turfing beer/wine
class Turf(models.Model):

    # user info
    turf_user = models.ForeignKey(User, on_delete=models.CASCADE)
    turf_to = models.CharField(max_length=30)
    turf_by = models.CharField(max_length=30)

    # turf details
    turf_time = models.DateTimeField(default=timezone.now)
    turf_note = models.CharField(max_length=50, blank=True)

    turf_count = models.DecimalField(decimal_places=2, max_digits=5)
    turf_type = models.CharField(max_length=10)


# model to account for boetes
class Boete(models.Model):

    # user info
    boete_user = models.ForeignKey(User, on_delete=models.CASCADE)
    boete_name = models.CharField(max_length=30)

    # boete details
    created_by = models.CharField(max_length=30)
    created_time = models.DateTimeField(default=timezone.now)

    boete_count = models.IntegerField(default=1)
    boete_note = models.CharField(max_length=100)

    @staticmethod
    def aggregate_user_fines(latest_date):
        result = Boete.objects.filter(created_time__gt=latest_date) \
            .values('boete_user_id') \
            .order_by('boete_user_id') \
            .annotate(boete_sum=Sum('boete_count'))

        return result
