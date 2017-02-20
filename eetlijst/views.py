from django.contrib.auth.models import User
from django.http import HttpResponse,JsonResponse
from user.models import Housemate
from eetlijst.models import HOLog, Transfer, DateList, UserList
from django.shortcuts import render, redirect
from django.utils import timezone
import datetime as dt
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse

# generate eetlijst view for current or defined date
def index(request, year=None, month=None, day=None):

    # get current date if nothing specified
    if not year or not month or not day:
        # bug solved; needed zero-pad to keep consistency in template context.focus_date
        year=str(timezone.now().year).zfill(2)
        month=str(timezone.now().month).zfill(2)
        day=str(timezone.now().day).zfill(2)

    # build date array
    focus_date = dt.date(int(year), int(month), int(day))
    prev_monday = focus_date - dt.timedelta(days=focus_date.weekday())

    # check if user has costs to fill
    open_days = []
    if request.user.is_authenticated():
        try:
            open_costs = DateList.objects.filter(cook=request.user).filter(cost=None).filter(open=False).order_by('date')

            if open_costs:
                user_open = True

                for oc in open_costs:
                    # url_date = oc.date.isoformat().replace('-','/')
                    open_days += [[oc.date.isoformat(),
                                   oc.date.strftime('%a (%d/%m)').replace('Mon','Ma').replace('Tue','Di').replace('Wed','Wo').replace('Thu','Do').replace('Fri','Vr').replace('Sat','Za').replace('Sun','Zo'),
                                   oc.date]]

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

    # combine date_list and database Userlist to reduce template tag queries
    date_entries = {}
    user_date_entries = {}
    for date in date_list:
        date_entries[date] = UserList.objects.filter(list_date=date_list[date][1])
        for entry in date_entries[date]:
            user_date_entries[ (entry.user_id, date_list[date][1]) ] = entry

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
        'user_date_entries': user_date_entries,
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
            messages.error(request, 'Invalid date.')

        return redirect('/eetlijst/' + sel_date[0:10] + '/')


# handle add ho requests
def add_ho(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            user_id = int(request.user.id)
            note = request.POST.get('note')

             # validate form input
            if request.POST.get('amount') == '':
                messages.error(request, 'Must add amount.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            if note == '':
                messages.error(request, 'Must add description.')
                return redirect(request.META.get('HTTP_REFERER'))

            # update housemate object for current user
            h = Housemate.objects.get(user_id=user_id)
            h.balance += amount
            h.save()

            # update housemate objects for other users
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
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle balance transfer post requests
def bal_transfer(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            current_user = int(request.user.id)
            other_user = request.POST.get('housemate')

             # validate form input
            if int(request.POST.get('housemate')) == 0:
                messages.error(request, 'Must choose housemate.')
                return redirect(request.META.get('HTTP_REFERER'))
            if request.POST.get('amount') == '':
                messages.error(request, 'Must add amount.')
                return redirect(request.META.get('HTTP_REFERER'))
            elif Decimal(request.POST.get('amount')) < 0:
                messages.error(request, 'Amount must be positive, use arrow button to choose direction.')
                return redirect(request.META.get('HTTP_REFERER'))
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
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst enrollment
def enroll(request):

    if request.method == 'POST':
        # Get user and turf type from POST
        breakOff = False
        try:
            user_id = request.POST.get('user_id')
        except:
            breakOff = True

        if user_id is None:
            # TODO: Should not occur without debug
            return HttpResponse(JsonResponse(
                {'result': 'Error: Could not find requested user.', 'status': 'failure'}))

        if request.user.is_authenticated():
            enroll_user = Housemate.objects.get(user_id=user_id)
            enroll_date = request.POST.get('enroll_date')
            enroll_type = request.POST.get('enroll_type')

            # get or create rows as necessary
            user_entry, user_created = UserList.objects.get_or_create(user=enroll_user.user, list_date=enroll_date)
            date_entry, date_created = DateList.objects.get_or_create(date=enroll_date)

            # modify models as appropriate
            if enroll_type == 'signup':
                user_entry.list_count += 1
                date_entry.num_eating += 1
                type_amount = user_entry.list_count
                if date_entry.open:
                    if user_entry.list_count == 1:
                        success_message = '%s is ingeschreven.' % (str(enroll_user).capitalize())
                    else:
                        success_message = '%s is %s keer ingeschreven.' % (str(enroll_user).capitalize(), int(user_entry.list_count))
                else:
                    # TODO: restyle instead of suggesting to refresh
                    return HttpResponse(JsonResponse({'result': 'There list is closed already. Please refresh page.', 'status': 'failure'}))
            elif enroll_type == 'sponge':
                date_entry.num_eating -= user_entry.list_count
                user_entry.list_count = 0
                if date_entry.open:
                    success_message = '%s is uitgeschreven.' % (str(enroll_user).capitalize())
                    type_amount = 0
                else:
                    # TODO: restyle instead of suggesting to refresh
                    return HttpResponse(JsonResponse(
                        {'result': 'There list is closed already. Please refresh page.', 'status': 'failure'}))
            elif enroll_type == 'cook':
                if date_entry.cook and not date_entry.cook == enroll_user.user:
                    return HttpResponse(JsonResponse({'result': 'There is already a cook.', 'status': 'failure'}))
                elif date_entry.cook == enroll_user.user:
                    user_entry.list_cook = False
                    date_entry.num_eating -= 1
                    date_entry.cook = None
                    date_entry.signup_time = None
                    success_message = '%s kookt niet meer.' % (str(enroll_user).capitalize())
                    type_amount = 0
                else:
                    user_entry.list_cook = True
                    date_entry.signup_time = timezone.now()
                    date_entry.cook = enroll_user.user
                    date_entry.num_eating += 1
                    success_message = '%s kookt voor het huis.' % (str(enroll_user).capitalize())
                    type_amount = 1
            else:
                return HttpResponse(JsonResponse({'result': 'Invalid submit button.', 'status': 'failure'}))

            user_entry.timestamp = timezone.now()
            user_entry.save()
            date_entry.save()

            # clean up if necessary
            if user_entry.list_count == 0 and user_entry.list_cook == False:
                user_entry.delete()

            if date_entry.num_eating == 0:
                date_entry.delete()

            # collect json data for jquery to check
            try:
                type_amount
            except:
                type_amount = False

            # Can be practical for cook sign-in
            signed_in_user = request.user.id

            json_data = {'result': success_message,
                         'login_user': signed_in_user,
                         'status': 'success',
                         'enroll_user': str(enroll_user),
                         'enroll_date': str(enroll_date),
                         'enroll_type': str(enroll_type),
                         'enroll_amount': str(type_amount),
                         'total_amount': str(date_entry.num_eating)}

            return HttpResponse(JsonResponse(json_data))
        else:
            return HttpResponse(JsonResponse({'result': 'Error: User not authenticated. Please log in again.', 'status': 'failure'}))
    else:
        messages.error(request, 'Method must be POST.')
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
                        messages.error(request, 'Must be cook to close list.')
                        return redirect(request.META.get('HTTP_REFERER'))

                else:

                    if not date_entry.cook == request.user:
                        messages.error(request, 'Must be cook to reopen list.')
                        return redirect(request.META.get('HTTP_REFERER'))

                    # Reverse existing costs
                    cost_amount = -date_entry.cost

                    # update housemate objects for users who signed up
                    huis = Housemate.objects.get(display_name='Huis')

                    remainder = huis.balance
                    split_cost = Decimal(round((cost_amount - remainder)/date_entry.num_eating,2))
                    huis.balance = date_entry.num_eating*split_cost - cost_amount + remainder


                    # update userlist objects
                    try:
                        users_enrolled = UserList.objects.filter(list_date=date_entry.date)
                    except UserList.DoesNotExist:
                        messages.error(request, 'No users signed up for selected date.')
                        return redirect(request.META.get('HTTP_REFERER'))

                    for u in users_enrolled:
                        h = Housemate.objects.get(user=u.user)

                        h.balance -= u.list_count*split_cost

                        if u.list_cook:
                            h.balance -= split_cost

                        u.list_cost = None

                        u.save()
                        h.save()

                    huis.save()

                    # update housemate object for current user
                    cook = Housemate.objects.get(user=request.user)
                    cook.balance += cost_amount
                    cook.save()

                    # add cost to log
                    date_entry.cost = None
                    date_entry.open = True
                    date_entry.close_time = None
                    date_entry.save()

                    messages.info(request, 'List re-opened, costs have been refunded.')
                    return redirect(request.META.get('HTTP_REFERER'))

            else:
                messages.error(request, 'Cannot close list without cook.')
                return redirect(request.META.get('HTTP_REFERER'))


        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst cost input
def cost(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get date from post
            date = request.POST.get('cost-date')

            # validate form input
            if request.POST.get('cost-amount') == '':
                messages.error(request, 'Must add amount.')
                return redirect(request.META.get('HTTP_REFERER'))
            elif Decimal(request.POST.get('cost-amount')) < 0:
                messages.error(request, 'Amount must be positive.')
                return redirect(request.META.get('HTTP_REFERER'))
            elif Decimal(request.POST.get('cost-amount')) > 999:
                messages.error(request, 'Amount must less than 999 euro''s.')
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                cost_amount = Decimal(round(Decimal(request.POST.get('cost-amount')), 2))

            # get or create rows as necessary
            try:
                date_entry = DateList.objects.get(date=date)

            except DateList.DoesNotExist:
                messages.error(request, 'No vaild entry for date.')
                return redirect(request.META.get('HTTP_REFERER'))
            if date_entry.num_eating <= 1:
                messages.error(request, "You can't cook for yourself moron. Well, you technically can. But not here. We don't allow it...  This is awkward.     Achievement: can't stop me #1")
                return redirect(request.META.get('HTTP_REFERER'))

            try:
                users_enrolled = UserList.objects.filter(list_date=date)
            except UserList.DoesNotExist:
                messages.error(request, 'No users signed up for selected date.')
                return redirect(request.META.get('HTTP_REFERER'))

            if date_entry.cook:
                try:
                    if date_entry.cost is None:
                        # add cost to log
                        print(date_entry.cost)
                        print(cost_amount)
                        date_entry.cost = cost_amount
                        print(date_entry.cost)
                    else:
                        messages.error(request, 'Server received cost fill-in for eetlijst, which has been previously multiple times.')
                        raise AssertionError

                    # update housemate object for current user
                    h = Housemate.objects.get(user=request.user)
                    h.balance += cost_amount

                    # update housemate objects for users who signed up
                    huis = Housemate.objects.get(display_name='Huis')

                    remainder = huis.balance
                    split_cost = Decimal(round((cost_amount - remainder)/date_entry.num_eating,2))
                    huis.balance = date_entry.num_eating*split_cost - cost_amount + remainder

                    # Seperately save
                    date_entry.save()
                    h.save()
                    huis.save()

                    # update userlist objects
                    for u in users_enrolled:
                        h = Housemate.objects.get(user=u.user)

                        h.balance -= u.list_count*split_cost
                        u.list_cost = -1*u.list_count*split_cost

                        if u.list_cook:
                            h.balance -= split_cost
                            u.list_cost = cost_amount - split_cost*(1+u.list_count)

                        u.save()
                        h.save()

                    h = Housemate.objects.get(user=request.user)

                except:
                    messages.error(request, 'Server internal error during calculation of cost.')

            else:
                messages.error(request, 'Cannot input cost without cook.')
                return redirect(request.META.get('HTTP_REFERER'))


        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# view for ho log
def ho_log(request, page=1):

    # get list of turfed items
    ho_list = Paginator(HOLog.objects.order_by('-time'), 25)

    # ensure page number is valid
    try:
        table_list = ho_list.page(page)
    except EmptyPage:
        table_list = ho_list.page(1)
        page = 1

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'table_list': table_list,
        'pages': str(ho_list.num_pages),
        'page_num': page
    }

    return render(request, 'eetlijst/ho_log.html', context)


# view for transfer log
def transfer_log(request, page=1):

    # get list of turfed items
    transfer_list = Paginator(Transfer.objects.order_by('-time'), 25)

    # ensure page number is valid
    try:
        table_list = transfer_list.page(page)
    except EmptyPage:
        table_list = transfer_list.page(1)
        page = 1

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'table_list': table_list,
        'pages': str(transfer_list.num_pages),
        'page_num': page
    }

    return render(request, 'eetlijst/transfer_log.html', context)