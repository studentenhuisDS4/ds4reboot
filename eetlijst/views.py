from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render
from django.utils import timezone
import datetime as dt
from django.shortcuts import redirect
from django.http import HttpResponse


# generate eetlijst view for current or defined date

def index(request, year=timezone.now().year, month=timezone.now().month, day=timezone.now().day):

    # build date array
    focus_date = dt.date(int(year), int(month), int(day))
    prev_monday = focus_date - dt.timedelta(days=focus_date.weekday())

    day_names = ['Ma','Di','Wo','Do','Vr','Za','Zo']
    date_list = {}

    for n in range(7):
        n_date = prev_monday + dt.timedelta(days=n)

        if n_date == focus_date:
            date_list[n] = [day_names[n], n_date, True]
        else:
            date_list[n] = [day_names[n], n_date, False]

    # get next/prev week
    week_p = focus_date - dt.timedelta(days=7)
    week_n = focus_date + dt.timedelta(days=7)
    day_p = focus_date - dt.timedelta(days=1)
    day_n = focus_date + dt.timedelta(days=1)

    date_nav = {}
    date_nav['pw'] = '/eetlijst/' + str(week_p.year) + '/' + str(week_p.month).zfill(2) + '/' + str(week_p.day).zfill(2) + '/'
    date_nav['nw'] = '/eetlijst/' + str(week_n.year) + '/' + str(week_n.month).zfill(2) + '/' + str(week_n.day).zfill(2) + '/'
    date_nav['pd'] = '/eetlijst/' + str(day_p.year) + '/' + str(day_p.month).zfill(2) + '/' + str(day_p.day).zfill(2) + '/'
    date_nav['nd'] = '/eetlijst/' + str(day_n.year) + '/' + str(day_n.month).zfill(2) + '/' + str(day_n.day).zfill(2) + '/'

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    # calculate total balance
    total_balance = 0
    for u in user_list:
        total_balance += u.balance

    # build context object
    context = {
        'breadcrumbs': ['eetlijst'],
        'user_list': user_list,
        'date_list': date_list,
        'date_nav': date_nav,
        'total_balance': total_balance,
    }

    return render(request, 'eetlijst/index.html', context)


# handle goto date post requests
def goto_date(request):

    # validate input
    sel_date = request.POST.get('date')

    if sel_date == '':
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        try:
            dt.date(int(sel_date[0:4]),int(sel_date[5:7]),int(sel_date[8:10]))
        except ValueError:
            return HttpResponse("Invalid date.")

        return redirect('/eetlijst/' + sel_date[0:10] + '/')