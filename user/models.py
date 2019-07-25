from decimal import Decimal

from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models

# model for housemates (linked to auth user)
from base.models import SoftDeletionModel


def get_active_users():
    return User.objects.filter(is_active=True).exclude(username__in=['huis', 'admin']).order_by(
        'housemate__movein_date')


# TODO untested
def get_total_balance():
    total_balance = 0
    for u in get_active_users():
        total_balance += u.housemate.balance

    total_balance += Housemate.objects.get(display_name='Huis').balance
    return total_balance


class Housemate(SoftDeletionModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=12)

    # logistics
    room_number = models.IntegerField(null=True)
    movein_date = models.DateField(default=timezone.now)
    moveout_date = models.DateField(null=True)

    # flag user for moveout (null=normal, false=ready for deletion, true=deleted)
    moveout_set = models.NullBooleanField()

    # phone numbers
    cell_phone = models.CharField(default='06', max_length=50)
    parent_phone = models.CharField(max_length=50, blank=True)

    # eetlijst related values
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    diet = models.CharField(max_length=100, blank=True)

    # store boete counts and status
    boetes_open = models.IntegerField(default=0)
    boetes_geturfd_rwijn = models.IntegerField(default=0)
    boetes_geturfd_wwijn = models.IntegerField(default=0)
    boetes_total = models.IntegerField(default=0)

    # store bottle counts since last HR
    sum_bier = models.IntegerField(default=0)
    sum_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    sum_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # store total bottle counts
    total_bier = models.IntegerField(default=0)
    total_wwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)
    total_rwijn = models.DecimalField(default=0, decimal_places=2, max_digits=8)

    # sum wine columns
    def get_sum_wijn(self):
        return self.sum_wwijn + self.sum_rwijn

    def get_total_wijn(self):
        return self.total_wwijn + self.total_rwijn

    sum_wijn = property(get_sum_wijn)
    total_wijn = property(get_total_wijn)

    def __str__(self):
        return self.display_name


def share_cost(housemates, cost, hm_payback):
    if len(housemates) < 2:
        raise ValueError("Not enough people to split")
    else:
        num_split = len(housemates)

    house_hm = Housemate.objects.get(display_name='Huis')
    remainder = house_hm.balance
    split_cost = Decimal(round((cost - remainder) / num_split, 2))
    house_hm.balance = num_split * split_cost - cost + remainder

    # TODO check balances and LOG to file
    total_balance_before = get_total_balance()

    # update userdinner set belonging to dinner
    for housemate in housemates:
        if hm_payback and housemate.id == hm_payback.id:
            housemate.balance -= split_cost - cost
        else:
            housemate.balance -= split_cost
        housemate.save()
    house_hm.save()

    # TODO check balances and LOG to file
    total_balance_after = get_total_balance()

    return {
        'split_cost': split_cost,
        'delta_remainder': house_hm.balance - remainder,
        'total_balance_before': total_balance_before,
        'total_balance_after': total_balance_after
    }
