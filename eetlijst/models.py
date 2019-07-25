from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from user.models import Housemate, get_total_balance


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

    def share_cost(self, cost):
        if self.cost:
            self.unshare_cost()
        if not self.num_eating:
            raise ValueError("num_eating incorrect value")
        if self.open:
            raise ValueError("dinner still open")

        dinner_uds = self.userdinner_set.all()

        # update housemate objects for users who signed up
        house_hm = Housemate.objects.get(display_name='Huis')
        remainder = house_hm.balance
        split_cost = Decimal(round((cost - remainder) / self.num_eating, 2))
        house_hm.balance = self.num_eating * split_cost - cost + remainder

        # TODO check balances and LOG to file
        total_balance_before = get_total_balance()

        # update userdinner set belonging to dinner
        for dinner_ud in dinner_uds:
            hm = dinner_ud.user.housemate
            hm.balance -= dinner_ud.count * split_cost
            dinner_ud.split_cost = -1 * dinner_ud.count * split_cost

            if dinner_ud.is_cook:
                hm.balance -= split_cost - cost
                dinner_ud.split_cost = cost - split_cost * (1 + dinner_ud.count)

            dinner_ud.save()
            hm.save()
        house_hm.save()

        # TODO check balances and LOG to file
        total_balance_after = get_total_balance()

        self.cost = cost
        self.cost_time = timezone.now()

        return {
            'delta_remainder': house_hm.balance - remainder,
            'total_balance_before': total_balance_before,
            'total_balance_after': total_balance_after}

    def unshare_cost(self):
        if not self.cost:
            return
        if not self.num_eating:
            raise ValueError("num_eating incorrect value (0)")
        if self.open:
            raise ValueError("dinner still open")
        self.userdinner_set.all()

        # Reverse existing costs
        cost_revert = -self.cost

        # TODO check balances and LOG to file
        total_balance_before = get_total_balance()

        # update housemate objects for users who signed up
        house_hm = Housemate.objects.get(display_name='Huis')
        remainder = house_hm.balance
        split_cost_inv = Decimal(round((cost_revert - remainder) / self.num_eating, 2))
        house_hm.balance = self.num_eating * split_cost_inv - cost_revert + remainder

        dinner_uds = self.userdinner_set.all()
        for dinner_ud in dinner_uds:
            hm = dinner_ud.user.housemate
            hm.balance -= dinner_ud.count * split_cost_inv
            if dinner_ud.is_cook:
                hm.balance += cost_revert - split_cost_inv
            dinner_ud.split_cost = None
            dinner_ud.save()
            hm.save()
        house_hm.save()

        # TODO check balances and LOG to file
        total_balance_after = get_total_balance()
        self.cost = None
        self.cost_time = None

        return {
            'delta_remainder': house_hm.balance - remainder,
            'total_balance_before': total_balance_before,
            'total_balance_after': total_balance_after}


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

    # full_detail = models.BooleanField(default=False)

    # debugging
    total_balance_after = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    total_balance_before = models.DecimalField(default=0, decimal_places=2, max_digits=4, null=True)
    delta_remainder = models.DecimalField(null=True, decimal_places=2, max_digits=5)
    affected_users = ArrayField(models.IntegerField(null=False), default=list)
