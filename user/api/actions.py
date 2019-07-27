from django.utils import timezone

from ds4admin.utils import send_moveout_mail
from ds4reboot.secret_settings import DEBUG
from eetlijst.models import SplitTransfer
from thesau.models import Report
from user.models import share_cost, Housemate, get_total_balance


def moveout_user(request, user):
    hms = Housemate.objects \
        .exclude(moveout_set=True) \
        .exclude(user_id=user.id) \
        .exclude(display_name__in=['Huis', 'Admin'])

    # finances
    pre_total = get_total_balance()
    share_cost(hms, -user.housemate.balance, hm_payback=user.housemate)
    users = [hm.user_id for hm in hms]
    users.sort()

    # administration
    user.is_active = False
    hm = user.housemate
    hm.moveout_date = timezone.now()
    hm.moveout_set = True
    hm.save()
    user.save()

    post_total = get_total_balance()
    split_transfer = SplitTransfer.objects.create(user=hm.user, amount=hm.balance, affected_users=users,
                                                  note='Verhuizen',
                                                  total_balance_before=pre_total, total_balance_after=post_total)

    # Send mail to thesau@ds4.nl, dale@ds4.nl
    last_hr_date = Report.objects.latest('report_date').report_date  # Assume housemate already lived here
    curr_date = timezone.now().date()
    est_hr_perc = round((curr_date - last_hr_date).days / 93.0 * 100, 2)
    if est_hr_perc > 100:
        est_hr_perc = 100
    if not DEBUG:
        send_moveout_mail(request, hm, last_hr_date, est_hr_perc, recipients=['thesau@ds4.nl', 'dale@ds4.nl'])
    else:
        print("Skipping mail because of DEBUG mode")

    return user, split_transfer
