import datetime as dt
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.decorators.http import require_POST

from eetlijst.models import SplitTransfer, Transfer, UserDinner, Dinner
from user.models import Housemate, get_total_balance


# generate eetlijst view for current or defined date
def index(request, year=None, month=None, day=None):
    # get current date if nothing specified
    if not year or not month or not day:
        # bug solved; needed zero-pad to keep consistency in template context.focus_date
        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

    # build date array
    focus_date = dt.date(int(year), int(month), int(day))
    prev_monday = focus_date - dt.timedelta(days=focus_date.weekday())

    # check if user has costs to fill
    open_days = []
    focus_close_date = None
    focus_close_cost = False
    if request.user.is_authenticated:
        try:
            open_costs = Dinner.objects.filter(cook=request.user).filter(cost=None).filter(open=False).order_by(
                'date')

            if open_costs:
                user_open = True

                for oc in open_costs:
                    # url_date = oc.date.isoformat().replace('-','/')
                    open_days += [[oc.date.isoformat(),
                                   oc.date.strftime('%a (%d/%m)')
                                       .replace('Mon', 'Ma')
                                       .replace('Tue', 'Di')
                                       .replace('Wed', 'Wo')
                                       .replace('Thu', 'Do')
                                       .replace('Fri', 'Vr')
                                       .replace('Sat', 'Za')
                                       .replace('Sun', 'Zo'),
                                   oc.date]]

            else:
                user_open = False

        except Dinner.DoesNotExist:
            user_open = False

    else:
        user_open = False

    # get open/closed status for week and check for cook
    try:
        focussed_date = Dinner.objects.get(date=focus_date)
        focus_open = focussed_date.open
        cook = Dinner.objects.get(date=focus_date).cook

        if cook:
            focus_cook = True
            if cook == request.user:
                focus_close_date = focus_date
                if focussed_date.cost is not None:
                    focus_close_cost = True
        else:
            focus_cook = False

    except Dinner.DoesNotExist:
        focus_open = True
        focus_cook = False

    # get dates for selected week
    day_names = ['Ma', 'Di', 'Wo', 'Do', 'Vr', 'Za', 'Zo']
    date_list = {}

    for n in range(7):
        n_date = prev_monday + dt.timedelta(days=n)

        try:
            open = Dinner.objects.get(date=n_date).open

        except Dinner.DoesNotExist:
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
    date_nav['pw'] = '/eetlijst/' + str(week_p.year) + '/' + str(week_p.month).zfill(2) + '/' + str(week_p.day).zfill(
        2) + '/'
    date_nav['nw'] = '/eetlijst/' + str(week_n.year) + '/' + str(week_n.month).zfill(2) + '/' + str(week_n.day).zfill(
        2) + '/'
    date_nav['pd'] = '/eetlijst/' + str(day_p.year) + '/' + str(day_p.month).zfill(2) + '/' + str(day_p.day).zfill(
        2) + '/'
    date_nav['nd'] = '/eetlijst/' + str(day_n.year) + '/' + str(day_n.month).zfill(2) + '/' + str(day_n.day).zfill(
        2) + '/'

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis').order_by('movein_date')

    # combine date_list and database Userlist to reduce template tag queries
    date_entries = {}
    user_date_entries = {}
    for date in date_list:
        date_entries[date] = UserDinner.objects.filter(dinner_date=date_list[date][1])
        for entry in date_entries[date]:
            user_date_entries[(entry.user_id, date_list[date][1])] = entry

    # get most recent HO items and transfers
    ho_list = SplitTransfer.objects.all().order_by('-id')[:5]
    tr_list = Transfer.objects.all().order_by('-id')[:5]

    # build context object
    context = {
        'breadcrumbs': ['eetlijst'],
        'user_list': user_list,
        'date_list': date_list,
        'user_date_entries': user_date_entries,
        'focus_date': str(year) + '-' + str(month) + '-' + str(day),
        'focus_cook': focus_cook,
        'focus_close_date': focus_close_date,
        'focus_close_date_new': focus_date,
        'focus_close_cost': focus_close_cost,
        'focus_open': focus_open,
        'user_open': user_open,
        'open_days': open_days,
        'date_nav': date_nav,
        'total_balance': get_total_balance(),
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
            dt.date(int(sel_date[0:4]), int(sel_date[5:7]), int(sel_date[8:10]))
        except ValueError:
            messages.error(request, 'Invalid date.')

        return redirect('/eetlijst/' + sel_date[0:10] + '/')


# handle add ho requests
@require_POST
def add_ho(request):
    if request.user.is_authenticated:

        user_id = int(request.user.id)
        note = request.POST.get('note')

        # validate form input
        if request.POST.get('amount') == '':
            messages.error(request, 'Must add amount.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            amount = Decimal(round(Decimal(request.POST.get('amount')), 2))

        if note == '':
            messages.error(request, 'Must add description.')
            return redirect(request.META.get('HTTP_REFERER'))

        # update housemate objects for other users
        huis = Housemate.objects.get(display_name='Huis')

        # Admin exclude are to be sure, admin shouldn't be active
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=None)
        active_housemates = Housemate.objects.filter(user__id__in=active_users) \
            .exclude(display_name='Huis') \
            .exclude(display_name='Admin')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .exclude(display_name__in=['Huis', 'Admin'])

        active_balance_before = 0
        for active_h in active_housemates:
            active_balance_before += active_h.balance
        inactive_balance = 0
        for inactive_h in inactive_housemates:
            inactive_balance += inactive_h.balance
        total_balance_before = active_balance_before + inactive_balance + huis.balance

        # take care of remainder
        remainder = huis.balance
        split_cost = round((amount - remainder) / len(active_housemates), 2)
        huis.balance = len(active_housemates) * split_cost - amount + remainder
        huis.save()

        # update housemate object for current active users
        h = Housemate.objects.get(user_id=user_id)
        for o in active_housemates:
            if o.id == h.id:
                o.balance += amount
            o.balance -= split_cost
            o.save()

        active_balance = 0
        for active_h in active_housemates:
            active_balance += active_h.balance

        overall_balance = active_balance + inactive_balance + huis.balance

        # add entry to ho table
        ho = SplitTransfer(
            user=h.user,
            amount=amount,
            note=note,
            total_balance_before=total_balance_before,
            total_balance_after=overall_balance)
        ho.save()

    else:
        return render(request, 'base/login_page.html')

    return redirect(request.META.get('HTTP_REFERER'))


# handle balance transfer post requests
@require_POST
def bal_transfer(request):
    if request.user.is_authenticated:

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
            amount = Decimal(round(Decimal(request.POST.get('amount')), 2))

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
        t = Transfer(
            user=request.user,
            from_user=from_user.user,
            to_user=to_user.user,
            amount=amount)
        t.save()

    else:
        return render(request, 'base/login_page.html')

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst enrollment
@require_POST
def enroll(request):
    # Get user and turf type from POST
    try:
        user_id = request.POST.get('user_id')
    except:
        return JsonResponse(
            {'result': 'Error: Could not find requested user.', 'status': 'failure'})

    if request.user.is_authenticated:
        enroll_user = Housemate.objects.get(user_id=user_id)
        enroll_date = request.POST.get('enroll_date')
        enroll_type = request.POST.get('enroll_type')

        # get or create rows as necessary
        dinner, date_created = Dinner.objects.get_or_create(date=enroll_date)
        dinner.save()
        user_entry, user_created = UserDinner.objects.get_or_create(user=enroll_user.user, dinner_date=dinner.date,
                                                                    dinner=dinner)

        # modify models as appropriate
        if enroll_type == 'signup':
            user_entry.count += 1
            dinner.num_eating += 1
            type_amount = user_entry.count
            if dinner.open:
                if user_entry.count == 1:
                    success_message = '%s is ingeschreven.' % (str(enroll_user).capitalize())
                else:
                    success_message = '%s is %s keer ingeschreven.' % (
                        str(enroll_user).capitalize(), int(user_entry.count))
            else:
                # TODO: restyle instead of suggesting to refresh
                return JsonResponse(
                    {'result': 'The list is closed already. Please refresh page.', 'status': 'failure'})
        elif enroll_type == 'sponge':
            dinner.num_eating -= user_entry.count
            user_entry.count = 0
            if dinner.open:
                success_message = '%s is uitgeschreven.' % (str(enroll_user).capitalize())
                type_amount = 0
            else:
                # TODO: restyle instead of suggesting to refresh
                return JsonResponse(
                    {'result': 'There list is closed already. Please refresh page.', 'status': 'failure'})
        elif enroll_type == 'cook':
            if dinner.cook and not dinner.cook == enroll_user.user:
                return JsonResponse({'result': 'There is already a cook.', 'status': 'failure'})
            elif dinner.cook == enroll_user.user:
                user_entry.is_cook = False
                dinner.num_eating -= 1
                dinner.cook = None
                dinner.cook_signup_time = None
                success_message = '%s kookt niet meer.' % (str(enroll_user).capitalize())
                type_amount = 0
            else:
                user_entry.is_cook = True
                dinner.cook_signup_time = timezone.now()
                dinner.cook = enroll_user.user
                dinner.num_eating += 1
                success_message = '%s kookt voor het huis.' % (str(enroll_user).capitalize())
                type_amount = 1
        else:
            return JsonResponse({'result': 'Invalid submit button.', 'status': 'failure'})

        user_entry.timestamp = timezone.now()
        user_entry.save()
        dinner.save()

        # clean up if necessary
        if user_entry.count == 0 and user_entry.is_cook == False:
            user_entry.delete()

        if dinner.num_eating == 0:
            dinner.delete()

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
                     'total_amount': str(dinner.num_eating)}

        return JsonResponse(json_data)

    else:
        return render(request, 'base/login_page.html')


# close eetlijst
@require_POST
def close(request):
    if request.user.is_authenticated:

        # get date from post
        date = request.POST.get('close-date')

        # get or create rows as necessary
        if date == 'None':
            messages.error(request,
                           "The given dinner date was not given. Now it is loaded you should try once more!")
            return redirect(request.META.get('HTTP_REFERER'))
        date_entry, date_created = Dinner.objects.get_or_create(date=date)

        if date_entry.cook:

            # check if cost is already entered
            if not date_entry.cost:

                if date_entry.cook == request.user:

                    # if open
                    if date_entry.open:
                        if date_entry.num_eating <= 1:
                            messages.error(request,
                                           "You can't cook for yourself. I mean, you can, but dont be stoopid.")
                            return redirect(request.META.get('HTTP_REFERER'))

                        date_entry.open = False
                        date_entry.close_time = timezone.now()
                        date_entry.save()

                        # Build up allergy string
                        userlist_entries = UserDinner.objects.filter(dinner_date=date)
                        allergy_status = ""

                        for userlist_entry in userlist_entries:
                            h = Housemate.objects.get(user_id=userlist_entry.user_id)
                            if h.diet:
                                allergy_status += h.display_name + " requires: " + h.diet.upper() + ". "

                        # Inform cook about allergy
                        if allergy_status:
                            messages.warning(request, allergy_status)

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
                split_cost = Decimal(round((cost_amount - remainder) / date_entry.num_eating, 2))
                huis.balance = date_entry.num_eating * split_cost - cost_amount + remainder

                # update userlist objects
                try:
                    users_enrolled = UserDinner.objects.filter(dinner_date=date_entry.date)
                except UserDinner.DoesNotExist:
                    messages.error(request, 'No users signed up for selected date.')
                    return redirect(request.META.get('HTTP_REFERER'))

                for u in users_enrolled:
                    h = Housemate.objects.get(user=u.user)

                    h.balance -= u.count * split_cost

                    if u.is_cook:
                        h.balance -= split_cost

                    u.split_cost = None

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

    return redirect(request.META.get('HTTP_REFERER'))


# handle eetlijst cost input
@require_POST
def cost(request):
    if request.user.is_authenticated:
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
            date_entry = Dinner.objects.get(date=date)

        except Dinner.DoesNotExist:
            messages.error(request, 'No vaild entry for date.')
            return redirect(request.META.get('HTTP_REFERER'))
        if date_entry.num_eating <= 1:
            messages.error(request,
                           "You can't cook for yourself. Achievement: can't stop me #1")
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            users_enrolled = UserDinner.objects.filter(dinner_date=date)
        except UserDinner.DoesNotExist:
            messages.error(request, 'No users signed up for selected date.')
            return redirect(request.META.get('HTTP_REFERER'))

        # use huis account to buffer small unsplittable amounts
        huis = Housemate.objects.filter(display_name='Huis').first()
        if huis == None:
            messages.error(request, 'Cannot split cost without a Huis account.')
            return redirect(request.META.get('HTTP_REFERER'))

        if date_entry.cook:
            try:
                if date_entry.cost is None:
                    # add cost to log
                    date_entry.cost = cost_amount
                else:
                    messages.error(request,
                                   'Server received cost fill-in for a day, which was already filled.')
                    raise AssertionError

                # update housemate object for current user
                hm = Housemate.objects.get(user=request.user)
                hm.balance += cost_amount

                remainder = huis.balance
                split_cost = Decimal(round((cost_amount - remainder) / date_entry.num_eating, 2))
                huis.balance = date_entry.num_eating * split_cost - cost_amount + remainder

                # Seperately save
                date_entry.save()
                hm.save()
                huis.save()

                # update userlist objects
                for u in users_enrolled:
                    hm = Housemate.objects.get(user=u.user)

                    hm.balance -= u.count * split_cost
                    u.split_cost = -1 * u.count * split_cost

                    if u.is_cook:
                        hm.balance -= split_cost
                        u.split_cost = cost_amount - split_cost * (1 + u.count)

                    u.save()
                    hm.save()
            except Exception as e:
                messages.error(request, 'Server internal error during calculation of cost.')
        else:
            messages.error(request, 'Cannot input cost without cook.')
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, 'base/login_page.html')

    return redirect(request.META.get('HTTP_REFERER'))


# view for ho log
def ho_log(request, page=1):
    active_users = User.objects.filter(is_active=True)
    active_housemates = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')
    select_housemates = active_housemates.exclude(display_name='Admin').exclude(display_name='Huis')

    filters = dict()
    filters_str = ['housemate',
                   'min_amount',
                   'sum_choice',
                   'final_date']
    sum_types = [
        {"option": 'aggregate_days', "label": 'Aggregate days'},
        {"option": 'aggregate_months', "label": 'Aggregate months'},
        {"option": 'aggregate_years', "label": 'Aggregate years'},
    ]

    for filt in filters_str:
        filters[filt] = request.GET.get(filt, 0)

    ho_logs = SplitTransfer.objects.order_by('-time')

    try:
        if int(filters['housemate']):
            u = User.objects.get(id=int(filters['housemate']))
            ho_logs = ho_logs.filter(user_id=u)
        if filters['min_amount']:
            ho_logs = ho_logs.filter(amount__gte=int(filters['min_amount']))
        if filters['final_date']:
            date = datetime.strptime(filters['final_date'], "%d-%m-%Y").date()
            ho_logs = ho_logs.filter(time__lte=date)
        if filters['sum_choice'] == "aggregate_days":
            ho_logs = ho_logs.extra(select={'time': 'date( time )'}) \
                .values('time', 'user__first_name') \
                .annotate(amount=Sum('amount')).order_by('-turf_time')
        elif filters['sum_choice'] == "aggregate_months":
            ho_logs = ho_logs.extra(select={'time': 'date( time )'}) \
                .extra({"month": "date_part(\'month\', \"time\")"}) \
                .extra({"year": "date_part(\'year\', \"time\")"}) \
                .values('month', 'year', 'user__first_name') \
                .annotate(amount=Sum('amount')).order_by('-year', '-month')
        elif filters['sum_choice'] == "aggregate_years":
            ho_logs = ho_logs.extra(select={'time': 'date( time )'}) \
                .extra({"year": "date_part(\'year\', \"time\")"}) \
                .values('user__first_name', 'year') \
                .annotate(amount=Sum('amount')).order_by('-year')
    except Exception as e:
        print("Exception:" + str(e))
        # pass

    # get list of turfed items
    ho_list = Paginator(ho_logs.order_by('-time'), 25)

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
        'housemates': select_housemates,
        'filters': filters,
        'sum_types': sum_types,
        'pages': str(ho_list.num_pages),
        'page_num': page
    }

    return render(request, 'eetlijst/ho/ho_log.html', context)


# view for transfer log
def transfer_log(request, page=1):
    active_users = User.objects.filter(is_active=True)
    active_housemates = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')
    select_housemates = active_housemates.exclude(display_name='Admin').exclude(display_name='Huis')

    filters = dict()
    filters_str = ['housemate_from', 'housemate_to',
                   'min_amount',
                   'sum_choice',
                   'final_date']
    sum_types = [
        {"option": 'aggregate_days', "label": 'Aggregate days'},
        {"option": 'aggregate_months', "label": 'Aggregate months'}
    ]

    for filt in filters_str:
        filters[filt] = request.GET.get(filt, 0)

    t_logs = Transfer.objects.order_by('-time')

    try:
        if int(filters['housemate_from']):
            h = Housemate.objects.get(id=int(filters['housemate_from']))
            t_logs = t_logs.filter(from_user=h)
        if int(filters['housemate_to']):
            h = Housemate.objects.get(id=int(filters['housemate_to']))
            t_logs = t_logs.filter(to_user=h)
        if filters['min_amount']:
            t_logs = t_logs.filter(amount__gte=int(filters['min_amount']))
        if filters['final_date']:
            date = datetime.strptime(filters['final_date'], "%d-%m-%Y").date()
            t_logs = t_logs.filter(time__lte=date)
        if filters['sum_choice'] == "aggregate_days":
            t_logs = t_logs.extra(select={'time': 'date( time )'})
            if int(filters['housemate_to']) and not int(filters['housemate_from']):
                t_logs = t_logs.values('time', 'from_user')
            elif int(filters['housemate_from']):
                t_logs = t_logs.values('time', 'to_user')
            else:
                t_logs = t_logs.values('time', 'to_user', 'from_user')
            t_logs = t_logs.annotate(amount=Sum('amount')).order_by('-turf_time')
        elif filters['sum_choice'] == "aggregate_months":
            t_logs = t_logs.extra(select={'time': 'date( time )'}) \
                .extra({"month": "date_part(\'month\', \"time\")"}) \
                .extra({"year": "date_part(\'year\', \"time\")"})
            if int(filters['housemate_to']) and not int(filters['housemate_from']):
                t_logs = t_logs.values('month', 'year', 'from_user')
            elif int(filters['housemate_from']):
                t_logs = t_logs.values('month', 'year', 'to_user')
            else:
                t_logs = t_logs.values('month', 'year', 'to_user', 'from_user')
            t_logs = t_logs.annotate(amount=Sum('amount')).order_by('-time')
    except Exception as e:
        print("Exception:" + str(e))
        pass

    # get list of turfed items
    transfer_list = Paginator(t_logs.order_by('-time'), 25)

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
        'housemates': select_housemates,
        'filters': filters,
        'sum_types': sum_types,
        'pages': str(transfer_list.num_pages),
        'page_num': page
    }

    return render(request, 'eetlijst/transfer/transfer_log.html', context)
