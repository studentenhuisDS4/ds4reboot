from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.views.decorators.http import require_POST, require_GET

from ds4admin.utils import check_dinners, check_moveout_dinners, check_dinners_housemate, send_moveout_mail
from ds4reboot.secret_settings import DEBUG
from user.models import Housemate
from eetlijst.models import SplitTransfer
from thesau.models import Report
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from decimal import Decimal


def test_mail(request):
    if DEBUG:
        return HttpResponse('Didnt send: DEBUG==True')

    if request.user.is_superuser:
        hm = Housemate.objects.get(display_name__exact='Dale')
        last_hr_date = datetime.now()
        est_hr_perc = 50
        send_moveout_mail(request, hm, last_hr_date, est_hr_perc, recipients=['dale@ds4.nl'])
        return HttpResponse('Sent')
    else:
        return HttpResponse('Denied')


# view for ds4 admin page
def balance(request):
    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users) \
            .exclude(display_name='Huis') \
            .exclude(display_name='Admin') \
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .exclude(moveout_set=True).order_by('movein_date').exclude(display_name='Admin')

        huis_balance = Housemate.objects.get(display_name='Huis').balance
        active_balance = 0
        for h in housemates:
            active_balance += h.balance

        inactive_balance = 0
        for h in inactive_housemates:
            inactive_balance += h.balance

        overall_balance = active_balance + inactive_balance + huis_balance

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'active_balance': active_balance,
            'inactive_balance': inactive_balance,
            'remainder': huis_balance,
            'overall_balance': overall_balance,
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
        }

        return render(request, 'ds4admin/balance.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')


def summary(request):
    active_users = User.objects.filter(is_active=True)
    inactive_users = User.objects.filter(is_active=False)
    housemates = Housemate.objects.filter(user__id__in=active_users).exclude(display_name='Huis') \
        .order_by('movein_date')
    inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
        .filter(moveout_set=None).order_by('movein_date').exclude(display_name='Admin')

    year = str(timezone.now().year).zfill(2)
    month = str(timezone.now().month).zfill(2)
    day = str(timezone.now().day).zfill(2)

    # build context object
    context = {
        'breadcrumbs': ['admin'],
        'housemates': housemates,
        'inactive': inactive_housemates,
        'current_day': timezone.now(),
        'focus_date': str(year) + '/' + str(month) + '/' + str(day),
    }
    return render(request, 'summary.html', context)


# view for huisgenooten tab
def housemates(request):
    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users) \
            .exclude(display_name='Huis') \
            .exclude(display_name='Admin') \
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .exclude(moveout_set=True).order_by('movein_date').exclude(display_name='Admin')

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        general_open_dinners, open_days = check_dinners(request)
        moveout_open_dinners, _ = check_moveout_dinners(request)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'current_day': timezone.now(),
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
            'moveout_open_dinners': moveout_open_dinners,
            'open_days': open_days,
            'general_open_dinners': general_open_dinners
        }

        return render(request, 'ds4admin/housemates.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')


# view for permissionstab
def permissions(request):
    if request.user.is_superuser:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        inactive_users = User.objects.filter(is_active=False)
        housemates = Housemate.objects.filter(user__id__in=active_users) \
            .exclude(display_name='Huis') \
            .exclude(display_name='Admin') \
            .order_by('movein_date')
        inactive_housemates = Housemate.objects.filter(user__id__in=inactive_users) \
            .exclude(moveout_set=True).order_by('movein_date').exclude(display_name='Admin')

        year = str(timezone.now().year).zfill(2)
        month = str(timezone.now().month).zfill(2)
        day = str(timezone.now().day).zfill(2)

        # build context object
        context = {
            'breadcrumbs': ['admin'],
            'housemates': housemates,
            'inactive': inactive_housemates,
            'current_day': timezone.now(),
            'focus_date': str(year) + '/' + str(month) + '/' + str(day),
        }

        return render(request, 'ds4admin/permissions.html', context)

    else:
        messages.error(request, 'Admin only area.')
        return redirect('/')


# handle requests to toggle user group
def toggle_group(request, group_type, user_id):
    u = User.objects.get(id=user_id)

    if group_type == 'admin':
        u.is_superuser ^= True
        u.is_staff ^= True
        u.save()

    elif group_type == 'thesau':

        g = Group.objects.get(name='thesau')

        if u.groups.filter(name='thesau').exists():
            g.user_set.remove(u)
        else:
            g.user_set.add(u)

    else:
        messages.error(request, 'Invalid group type.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle remove housemate post requests
def remove_housemate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            # get data from POST
            remove_id = int(request.POST.get('housemate'))
            hms = Housemate.objects.all()
            for hm in hms:
                print(hm, hm.user_id)
            hm = Housemate.objects.get(user_id=remove_id)
            unpayed_dinners = check_dinners_housemate(request, hm)
            safe_to_remove = True
            unsafe_string = ""
            for dinner in unpayed_dinners:
                if dinner.cook.is_active:
                    safe_to_remove = False
                    unsafe_string += f"(Cook: {dinner.cook.housemate.display_name}, date: {str(dinner.date)}), "

            if not safe_to_remove:
                messages.error(request,
                               f"You can\'t deactivate {hm.display_name}. Please check unsafe dinners: {unsafe_string}")
            elif not remove_id:
                messages.error(request, 'Must specify housemate to be removed.')
            else:
                # update housemate object
                hm.moveout_set = True
                hm.moveout_date = timezone.now()

                # So Django Authentication gives correct message (disabled account)
                u = hm.user
                u.is_active = False

                # Get required database objects
                huis = Housemate.objects.get(display_name='Huis')
                active_users = User.objects \
                    .filter(is_active=True) \
                    .exclude(id=remove_id) \
                    .exclude(username='huis') \
                    .exclude(username='admin')

                # Get coupled housemates
                other_housemates = Housemate.objects.filter(user__id__in=active_users)

                # Get old remainder and optimally calculate split cost to remove this housemate
                remainder = huis.balance

                split_cost = Decimal(round((hm.balance + remainder) / len(other_housemates), 2))
                total_diff = len(active_users) * split_cost
                new_remainder = -(total_diff - hm.balance)

                # Calculate the remainder for the house
                huis.balance += new_remainder

                # add log entry to eating list ho table
                ho = SplitTransfer(user=hm.user, amount=hm.balance, note='Verhuizen')

                # Render email to send summary
                last_hr_date = Report.objects.latest('report_date').report_date  # Assume housemate already lived here
                curr_date = timezone.now().date()

                # Force float by introducing comma: 93.0
                est_hr_perc = round((curr_date - last_hr_date).days / 93.0 * 100, 2)  # Assume 31 * 3 days for HR

                if est_hr_perc > 100:
                    est_hr_perc = 100

                # Perform all required update operations
                sum = 0
                for o in other_housemates:
                    o.balance += split_cost
                    sum += o.balance
                    o.save()

                hm.save()
                u.save()
                huis.save()
                ho.save()

                ##
                # SEND MOVEOUT MAIL
                # Targets: thesau@ds4.nl, dale@ds4.nl
                ##
                if not DEBUG:
                    send_moveout_mail(request, hm, last_hr_date, est_hr_perc, recipients=['thesau@ds4.nl', 'dale@ds4.nl'])
                else:
                    print("Skipping mail because of DEBUG mode")
        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle activation of inactive housemate
def activate_housemate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            # get data from POST
            try:
                activate_id = int(request.POST.get('housemate'))
            except TypeError:
                activate_id = None

            try:
                activate_date = request.POST.get('activate_date')
            except TypeError:
                activate_date = None

            if not activate_id:
                messages.error(request, 'Must specify housemate to be deactivated.')
            elif not activate_date:
                messages.error(request, 'No activation date given.')
            else:
                # update housemate object
                h = Housemate.objects.get(user_id=activate_id)

                # TODO: Consider setting inactivation date instead of move-out date
                h.moveout_set = None
                h.moveout_date = timezone.now()
                h.save()

                u = h.user
                u.is_active = True

                u.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle deactivation of housemate post requests
def deactivate_housemate(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            # get data from POST
            try:
                deactivate_id = int(request.POST.get('housemate'))
            except TypeError:
                deactivate_id = None

            try:
                deactivate_date = request.POST.get('deactivate_date')
                print(deactivate_date)
            except TypeError:
                deactivate_date = None

            if not deactivate_id:
                messages.error(request, 'Must specify housemate to be deactivated.')
            elif not deactivate_date:
                messages.error(request, 'Must specify deactivation date.')
            else:
                # update housemate object
                h = Housemate.objects.get(user_id=deactivate_id)
                h.moveout_set = False

                # TODO: Consider setting inactivation date instead of move-out date
                h.moveout_date = timezone.now()
                h.save()

                u = h.user
                u.is_active = False

                u.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


@require_GET
def create_user(request):
    # build context object
    context = {
        'breadcrumbs': ['admin', 'create user'],
    }

    return render(request, 'ds4admin/create_user.html', context)


@require_POST
def create_user_post(request):
    try:
        # Assume client side validation has succeeded
        email = request.POST.get("email", "")
        cellphone = request.POST.get("cellphone", "")
        parentphone = request.POST.get("parentphone", "")
        diet = request.POST.get("diet", "")
        room_number = request.POST.get("room-number", "")
        profile_name = request.POST.get("profile-name", "")
        first_name = request.POST.get("first-name", "")
        last_name = request.POST.get("last-name", "")
        new_pass = request.POST.get("new-pass", "")
        verify_pass = request.POST.get("verify-pass", "")

        if len(new_pass) == 0 and len(new_pass) > 5:
            messages.error(request, 'Nieuw wachtwoord is niet lang genoeg of niet gegeven.')
        elif len(verify_pass) == 0 and len(verify_pass) > 5:
            messages.error(request, 'Nieuw (herhaald) wachtwoord is niet lang genoeg of niet gegeven.')
        elif new_pass != verify_pass:
            messages.error(request, 'Nieuw (herhaald) wachtwoord is niet goed herhaald.')
        else:
            if email == "" or first_name == "" or last_name == "":
                messages.error(request, 'Email, first or last name empty.')
                return redirect(request.META.get('HTTP_REFERER'))
            if room_number == "":
                messages.error(request, 'Room number not specified.')
                return redirect(request.META.get('HTTP_REFERER'))

            if cellphone == "":
                messages.warning(request, 'Telephone empty.')
            if parentphone == "":
                messages.warning(request, 'Telephone parents empty.')
            if diet == "":
                messages.warning(request, 'Diet empty.')

            user = User.objects.create_user(email=email, username=profile_name, password=verify_pass,
                                            first_name=first_name, last_name=last_name)
            if user is not None:
                # Authenticate current password
                user_auth = authenticate(username=user.username, password=verify_pass)
                if user_auth is not None:
                    user_auth.save()
                else:
                    messages.error(request, 'The password did not validate.')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, 'The profile couldnt be created. User not created somehow.')
                return redirect(request.META.get('HTTP_REFERER'))

            # Define user, housemate to be created
            user.housemate = Housemate.objects.create(user_id=user.id, diet=diet,
                                                      cell_phone=cellphone, parent_phone=parentphone,
                                                      display_name=first_name,
                                                      room_number=room_number)
            user.housemate.save()
            user.save()

            messages.success(request, 'Profile for ' + profile_name + ' (' +
                             user.first_name + ') succesfull.')

            # get requested user
            return redirect('/user/profiel/' + str(user.id) + '/')

    except Exception as e:
        messages.error(request, 'The form couldnt be validated correctly. ' + str(e))

    return redirect(request.META.get('HTTP_REFERER'))
