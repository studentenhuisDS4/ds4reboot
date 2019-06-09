from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime

from eetlijst.models import DateList, UserList
from thesau.models import Report
from user.models import Housemate


def send_moveout_mail(request, hm, last_hr_date, est_hr_perc, recipients=['thesau@ds4.nl']):
    try:
        user = hm.user
        full_name = user.first_name + " " + user.last_name

        msg_html = render_to_string('email/thesau_mail_dynamic.html',
                                    {'full_name': full_name,
                                     'balance': str(hm.balance),
                                     'beers': str(hm.sum_bier),
                                     'red_wine': str(hm.sum_rwijn),
                                     'white_wine': str(hm.sum_wwijn),
                                     'fine_wine': str(hm.boetes_open),
                                     'fine_wine_turfed': str(hm.boetes_geturfd_rwijn + hm.boetes_geturfd_wwijn),
                                     'move_in_date': str(hm.movein_date),
                                     'move_out_date': datetime.now(),  # str(hm.moveout_date.date()),
                                     'last_hr_date': str(last_hr_date),
                                     'est_hr_perc': str(est_hr_perc)
                                     })
        send_mail(
            'DS4 housemate moved out - site report',
            full_name + ' left DS4. TXT mail is not supported. Use HTML instead.',
            'admin@ds4.nl',
            recipients,
            html_message=msg_html,
            fail_silently=False
        )
        messages.warning(request, f"Successfully sent mail to {recipients}")
    except Exception as e:
        messages.error(request, f"Error while sending mail to {recipients}: {str(e)}")


def check_dinners(request):
    open_days = DateList.objects.filter(open=False, cost__exact=None)
    general_open_dinners = dict()
    for day in open_days:
        userlist_day = UserList.objects.filter(list_date=day.date)
        if userlist_day is not None:
            general_open_dinners[day] = userlist_day

    return general_open_dinners, open_days


def check_moveout_dinners(request):
    open_days = DateList.objects.filter(open=False, cost__exact=None)
    moveout_list = Housemate.objects.filter(moveout_set=1).order_by('moveout_date')
    moveout_open_dinners = dict()

    if len(Report.objects.all()) > 0:
        latest_hr = Report.objects.latest('id')
    else:
        latest_hr = datetime.now()

    moveout_pending = []
    if moveout_list:
        for h in moveout_list:
            user_cost_days = []
            throw_warning = False
            if h.moveout_date >= latest_hr.report_date:
                moveout_pending.append(h)

                for day in open_days:
                    userlist_day = UserList.objects.filter(list_date=day.date, user_id=h.user_id).first()
                    if userlist_day is not None:
                        user_cost_days.append(day)
                        if day.cook.is_active:
                            throw_warning = True

                # Merge all data
                moveout_open_dinners[h] = user_cost_days

            # Build up warning
            if throw_warning and request is not None:
                messages.warning(request, 'User ' + h.display_name +
                                 f" has {len(user_cost_days)} active UNPAID dinners. "
                                 f"Please check this to avoid inconsistency on the TOTAL BALANCE.")
    return moveout_open_dinners, moveout_pending


def check_dinners_housemate(request, hm):
    open_days = DateList.objects.filter(open=False, cost__exact=None)
    open_days_user = []
    for day in open_days:
        userlist_day = UserList.objects.filter(list_date=day.date, user_id=hm.user_id)
        if len(userlist_day) == 1:
            open_days_user.append(day)
    return open_days_user
