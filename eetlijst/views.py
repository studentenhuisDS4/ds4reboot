from django.contrib.auth.models import User
from user.models import Housemate
from eetlijst.models import HOLog, Transfer, DateList, UserList
from django.shortcuts import render, redirect
from django.utils import timezone
import datetime as dt
from django.http import HttpResponse
from decimal import Decimal


# generate eetlijst view for current or defined date
def index(request, year=timezone.now().year, month=timezone.now().month, day=timezone.now().day):

    # build date array
    focus_date = dt.date(int(year), int(month), int(day))
    prev_monday = focus_date - dt.timedelta(days=focus_date.weekday())

    # check if user has costs to fill
    open_days = []
    if request.user.is_authenticated():
        try:
            open_costs = DateList.objects.filter(cook=request.user).filter(cost=None).filter(open=False)

            if open_costs:
                user_open = True

                for oc in open_costs:
                    open_days += [[oc.date.isoformat(), oc.date.strftime('%a (%d/%m)').replace('Mon','Ma').replace('Tue','Do').replace('Wed','Wo').replace('Thu','Do').replace('Fri','Vr').replace('Sat','Za').replace('Sun','Zo')]]

            else:
                user_open = False

        except DateList.DoesNotExist:
            user_open = False

    else:
        user_open = False


    # get open/closed status for week and check for cook
    try:
        focus_open = DateList.objects.get(date=focus_date).open
        cook = DateList.objects.get(date=focus_date).cook

        if cook:
            focus_cook = True
        else:
            focus_cook = False

    except DateList.DoesNotExist:
        focus_open = True
        focus_cook = False

    # get dates for selected week
    day_names = ['Ma','Di','Wo','Do','Vr','Za','Zo']
    date_list = {}

    for n in range(7):
        n_date = prev_monday + dt.timedelta(days=n)

        try:
            open = DateList.objects.get(date=n_date).open

        except DateList.DoesNotExist:
            open = True

        if n_date == focus_date:
            date_list[n] = [day_names[n], n_date, True, open]
        else:
            date_list[n] = [day_names[n], n_date, False, open]

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
    user_list = Housemate.objects.filter(user__id__in=active_users).exclude(display_name = 'Huis').order_by('movein_date')

    # calculate total balance
    total_balance = 0
    for u in user_list:
        total_balance += u.balance

    total_balance += Housemate.objects.get(display_name='Huis').balance

    # get most recent HO items and transfers
    ho_list = HOLog.objects.all().order_by('-id')[:5]
    tr_list = Transfer.objects.all().order_by('-id')[:5]

    # build context object
    context = {
        'breadcrumbs': ['eetlijst'],
        'user_list': user_list,
        'date_list': date_list,
        'focus_date': str(year) + '-' + str(month) + '-' + str(day),
        'focus_cook': focus_cook,
        'focus_open': focus_open,
        'user_open': user_open,
        'open_days': open_days,
        'date_nav': date_nav,
        'total_balance': total_balance,
        'ho_list': ho_list,
        'tr_list': tr_list,
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


# handle add ho requests
def add_ho(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            user_id = int(request.user.id)
            note = request.POST.get('note')

             # validate form input
            if request.POST.get('amount') == '':
                return HttpResponse("Must add amount.")
            else:
                amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            if note == '':
                return HttpResponse("Must add description.")

            # update housemate object for current user
            h = Housemate.objects.get(user_id=user_id)
            h.balance += amount
            h.save()

            #update housemate objects for other users
            huis = Housemate.objects.get(display_name='Huis')

            active_users = User.objects.filter(is_active=True)
            other_housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis')

            # take care of remainder
            remainder = huis.balance
            split_cost = round((amount - remainder)/len(other_housemates),2)
            huis.balance = len(other_housemates)*split_cost - amount + remainder

            huis.save()

            for o in other_housemates:
                o.balance -= split_cost
                o.save()

            # add entry to ho table
            ho = HOLog(user=h.user, amount=amount, note=note)
            ho.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))


# handle balance transfer post requests
def bal_transfer(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            current_user = int(request.user.id)
            other_user = request.POST.get('housemate')

             # validate form input
            if int(request.POST.get('housemate')) == 0:
                return HttpResponse("Must choose housemate.")

            if request.POST.get('amount') == '':
                return HttpResponse("Must add amount.")
            elif Decimal(request.POST.get('amount')) < 0:
                return HttpResponse("Amount must be positive. Use arrow button instead.")
            else:
                amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            # get user data from POST
            if request.POST.get('direction') == 'to':
                from_user = Housemate.objects.get(user_id=current_user)
                to_user = Housemate.objects.get(user_id=other_user)
            else:
                from_user = Housemate.objects.get(user_id=other_user)
                to_user = Housemate.objects.get(user_id=current_user)


            # update housemate objects
            from_user.balance -= amount
            from_user.save()

            to_user.balance += amount
            to_user.save()

            # add entry to transfer table
            t = Transfer(user=request.user, from_user=from_user.user.housemate.display_name, to_user=to_user.user.housemate.display_name, amount=amount)
            t.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst enrollment
def enroll(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get info from post
            sel_user = Housemate.objects.get(user_id=request.POST.get('enroll-user'))
            action = request.POST.get('enroll-action')
            date = request.POST.get('enroll-date')

            # get or create rows as necessary
            user_entry, user_created = UserList.objects.get_or_create(user=sel_user.user, list_date=date)
            date_entry, date_created = DateList.objects.get_or_create(date=date)

            # modify models as appropriate
            if action == 'eat':
                user_entry.list_count += 1
                date_entry.num_eating += 1

            elif action == 'cook':
                if date_entry.cook and not date_entry.cook == sel_user.user:
                    return HttpResponse("There is already a cook.")
                elif date_entry.cook == sel_user.user:
                    user_entry.list_cook = False
                    date_entry.num_eating -= 1
                    date_entry.cook = None
                    date_entry.signup_time = None
                else:
                    user_entry.list_cook = True
                    date_entry.signup_time = timezone.now()
                    date_entry.cook = sel_user.user
                    date_entry.num_eating += 1

            elif action == 'sponge':
                date_entry.num_eating -= user_entry.list_count
                user_entry.list_count = 0

            elif action == 'swap':
                date_entry.num_eating -= user_entry.list_count
                user_entry.list_count = 0

                if date_entry.cook and not date_entry.cook == sel_user.user:
                    return HttpResponse("There is already a cook.")
                elif date_entry.cook == sel_user.user:
                    user_entry.list_cook = False
                    date_entry.num_eating -= 1
                    date_entry.cook = None
                    date_entry.signup_time = None
                else:
                    user_entry.list_cook = True
                    date_entry.signup_time = timezone.now()
                    date_entry.cook = sel_user.user
                    date_entry.num_eating += 1

            else:
                return HttpResponse("Invalid submit button.")

            user_entry.timestamp = timezone.now()
            user_entry.save()
            date_entry.save()

            # clean up if necessary
            if user_entry.list_count == 0 and user_entry.list_cook == False:
                user_entry.delete()

            if date_entry.num_eating == 0:
                date_entry.delete()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))


# close eetlijst
def close(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get date from post
            date = request.POST.get('close-date')

            # get or create rows as necessary
            date_entry, date_created = DateList.objects.get_or_create(date=date)

            if date_entry.cook:

                # check if cost is already entered
                if not date_entry.cost:

                    if date_entry.cook == request.user:

                        # if open
                        if date_entry.open == True:
                            date_entry.open = False
                            date_entry.close_time = timezone.now()
                            date_entry.save()

                        # if closed
                        else:
                            date_entry.open = True
                            date_entry.close_time = None
                            date_entry.save()

                    else:
                        return HttpResponse("Must be cook to close list.")

                else:
                    return HttpResponse("Cannot reopen list once cost is entered.")

            else:
                return HttpResponse("Cannot close list without cook.")


        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst cost input
def cost(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get date from post
            date = request.POST.get('cost-date')

            # validate form input
            if request.POST.get('cost-amount') == '':
                return HttpResponse("Must add amount.")
            elif Decimal(request.POST.get('cost-amount')) < 0:
                return HttpResponse("Amount must be positive.")
            else:
                cost = Decimal(round(Decimal(request.POST.get('cost-amount')),2))

            # get or create rows as necessary
            try:
                date_entry = DateList.objects.get(date=date)

            except DateList.DoesNotExist:
                return HttpResponse("No vaild entry for date.")

            try:
                users_enrolled = UserList.objects.filter(list_date=date)

            except UsereList.DoesNotExist:
                return HttpResponse("No users signed up for selected date.")

            if date_entry.cook:

                # add cost to log
                date_entry.cost = cost
                date_entry.save()

                # update housemate object for current user
                h = Housemate.objects.get(user=request.user)
                h.balance += cost
                h.save()

                # update housemate objects for users who signed up
                huis = Housemate.objects.get(display_name='Huis')

                remainder = huis.balance
                split_cost = round((cost - remainder)/date_entry.num_eating,2)
                huis.balance = date_entry.num_eating*split_cost - cost + remainder

                huis.save()

                # update userlist objects
                for u in users_enrolled:
                    h = Housemate.objects.get(user=u.user)

                    h.balance -= u.list_count*split_cost
                    u.list_cost = -1*u.list_count*split_cost

                    if u.list_cook:
                        h.balance -= split_cost
                        u.list_cost = cost - split_cost*(1+u.list_count)

                    u.save()
                    h.save()

            else:
                return HttpResponse("Cannot input cost without cook.")


        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))