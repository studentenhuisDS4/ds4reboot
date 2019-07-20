from django.db.models import Sum
from rainbowtests import colors

from user.models import Housemate


def assert_total_balance():
    total_bal = Housemate.objects.filter(user__is_active=True).aggregate(Sum('balance'))['balance__sum']
    assert total_bal == 0
    print(colors.cyan("Balance correct: "), colors.blue(str(total_bal)))
