from django.contrib import messages
from django.utils.datetime_safe import datetime

from eetlijst.models import DateList, UserList
from thesau.models import Report
from user.models import Housemate


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
                                 f" has {len(user_cost_days)} active UNPAYED dinners. "
                                 f"Please check this to avoid inconsistency on the TOTAL BALANCE.")
    return moveout_open_dinners, moveout_pending


def check_dinners_housemate(request, hm):
    open_days = DateList.objects.filter(open=False, cost__exact=None)
    open_days_user = []
    for day in open_days:
        userlist_day = UserList.objects.filter(list_date=day.date, user_id= hm.user_id)
        if len(userlist_day) == 1:
            open_days_user.append(day)
    return open_days_user
