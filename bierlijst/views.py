from django.contrib.auth.models import User
from user.models import Housemate
from bierlijst.models import Turf, Boete
from thesau.models import BoetesReport
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from decimal import Decimal
from django.db.models import Sum, Q
from django.core.paginator import Paginator, EmptyPage
# from gcm.models import get_device_model
import json


# index view for bierlijst
def index(request):

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    # calculate turf totals
    totals = [str(list(user_list.aggregate(Sum('sum_bier')).values())[0]),
              str(list(user_list.aggregate(Sum('sum_wwijn')).values())[0] + list(user_list.aggregate(Sum('sum_rwijn')).values())[0]),
              str(list(user_list.aggregate(Sum('sum_wwijn')).values())[0]),
              str(list(user_list.aggregate(Sum('sum_rwijn')).values())[0]),
              str(list(user_list.aggregate(Sum('boetes_open')).values())[0])]

    # find medaled users
    user_medals = Housemate.objects.exclude(user__username='huis').filter(user__id__in=active_users).order_by('-sum_bier')[:3]
    medals = []

    for u in user_medals:
        if u.sum_bier > 0:
            medals += [u.user_id]
        else:
            medals += [0]

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'user_list': user_list,
        'totals': totals,
        'medals': medals,
    }

    return render(request, 'bierlijst/index.html', context)


# view for bierlijst log
def show_log(request, page=1):

    # get list of turfed items
    turf_list = Paginator(Turf.objects.order_by('-turf_time'), 25)

    # ensure page number is valid
    try:
        table_list = turf_list.page(page)
    except EmptyPage:
        table_list = turf_list.page(1)
        page = 1

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'table_list': table_list,
        'pages': str(turf_list.num_pages),
        'page_num': page
    }

    return render(request, 'bierlijst/log.html', context)


# view for boetes including form submission
def boetes(request, page=1):

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    housemates = Housemate.objects.filter(user__id__in = active_users).exclude(display_name = 'Huis').order_by('movein_date')

    # get lists of all boetes and users with open boetes
    log_boetes = Housemate.objects.filter(Q(boetes_open__gt = 0) | Q(boetes_geturfd__gt = 0), user__id__in = active_users).order_by('-boetes_open')
    num_boetes = str(list(log_boetes.filter(boetes_open__gt = 0).aggregate(Sum('boetes_open')).values())[0])
    boetes_list = Paginator(Boete.objects.order_by('-created_time'), 10)

    # ensure page number is valid
    try:
        table_list = boetes_list.page(page)
    except EmptyPage:
        table_list = boetes_list.page(1)
        page = 1

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'housemates': housemates,
        'log_boetes': log_boetes,
        'num_boetes': num_boetes,
        'table_list': table_list,
        'pages': str(boetes_list.num_pages),
        'page_num': page
    }

    return render(request, 'bierlijst/boetes.html', context)


# handle add boetes post requests
def add_boete(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            user_id = int(request.POST.get('housemate'))
            note = request.POST.get('note')

            if request.POST.get('count') == '':
                count = 1
            else:
                count = int(request.POST.get('count'))

            # validate form input
            if count > 10 or count < 1:
                messages.error(request, 'Number of boetes must be between 1 and 10.')
                return redirect(request.META.get('HTTP_REFERER'))
            if note == '':
                messages.error(request, 'Must add reason.')
                return redirect(request.META.get('HTTP_REFERER'))

            elif len(note) > 100:
                messages.error(request, 'Note must be less than 50 characters!')
                return redirect(request.META.get('HTTP_REFERER'))

            if user_id == 0:
                messages.error(request, 'Must choose housemate.')
                return redirect(request.META.get('HTTP_REFERER'))

            # update housemate object
            h = Housemate.objects.get(user_id=user_id)
            h.boetes_open += count
            h.boetes_total += count
            h.save()

            # add entry to boete table
            b = Boete(boete_user=h.user, boete_name=h.display_name, created_by=request.user, boete_count=count, boete_note=note)
            b.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# handle remove boete requests
def remove_boete(request, boete_id):

    if request.user.is_authenticated():
        b = Boete.objects.get(id=boete_id)

        h = Housemate.objects.get(user_id=b.boete_user)
        h.boetes_open -= b.boete_count
        h.boetes_total -= b.boete_count
        h.save()

        b.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'base/login_page.html')


# handle turf boete requests
def turf_boete(request, type_wine, user_id):

    if request.user.is_authenticated():

        if type_wine == 'r' or type_wine == 'w':

            # update housemate object
            h = Housemate.objects.get(user_id=user_id)
            h.boetes_open -= 1
            h.boetes_geturfd += 1
            h.save()

            # record type of wine
            t, _ = BoetesReport.objects.get_or_create(type=type_wine, defaults={'boete_count': 0})
            t.boete_count += 1
            t.save()

        else:
            messages.error(request, 'Invalid turf type.')

        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'base/login_page.html')


# handle reset boete requests
def reset_boetes(request):

    if request.user.is_authenticated():

        Boete.objects.all().delete()

        for h in Housemate.objects.all():
            h.boetes_open = 0
            h.boetes_geturfd = 0
            h.save()

        messages.error(request, 'Boetes have been reset.')
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, 'base/login_page.html')


# handle turf post requests
def turf_item(request, user_id):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # Get user and turf type from POST
            turf_user = User.objects.get(pk=user_id)
            turf_type = request.POST.get('turf_type')

            if request.POST.get('count'):

                # validate count input
                try:
                    turf_count = Decimal(round(Decimal(request.POST.get('count')), 2))

                except ValueError:
                    return HttpResponse(json.dumps({'result': 'Error: Count moet een nummer zijn.', 'status': 'failure'}))

                if turf_type == 'bier' and not float(turf_count).is_integer():
                    return HttpResponse(json.dumps({'result': 'Error: Je moet een heel biertje turven.', 'status': 'failure'}))

                if turf_count >= 1000:
                    return HttpResponse(json.dumps({'result': 'Error: Je kunt niet meer dan 999 items turven.', 'status': 'failure'}))

            else:
                turf_count = 1

            # print ('TURF | user: %s | type: %s | count: %s' % (turf_user, turf_type, turf_count))

            h = Housemate.objects.get(user_id=user_id)

            # add entry to database
            new_value = 0
            if turf_type == 'bier':
                if h.sum_bier + turf_count >= 0:
                    h.sum_bier += turf_count
                    h.total_bier += turf_count

                    success_message = '%s heeft %s bier geturft.' % (str(turf_user).capitalize(), int(turf_count))
                    success_message = success_message if turf_count == 1 else success_message.replace('bier', 'biertjes')
                else:
                    success_message = 'Je kan geen negatief aantal biertjes hebben.'
                    return HttpResponse(json.dumps({'result': success_message, 'status': 'failure'}))

                new_value = h.sum_bier
                new_value_total = h.total_bier

                # GCM testing (old)
                # device = get_device_model()
                # device.objects.all().send_message({'message':'my test message'})

            elif turf_type == 'wwijn':
                if h.sum_wwijn + turf_count >= 0:
                    h.sum_wwijn += Decimal(turf_count)
                    h.total_wwijn += Decimal(turf_count)

                    success_message = '%s heeft %s witte wijn geturft.' % (str(turf_user).capitalize(), turf_count)
                else:
                    success_message = 'Je kan geen negatief aantal wijnflessen hebben.'
                    return HttpResponse(json.dumps({'result': success_message, 'status': 'failure'}))

                new_value = h.sum_wwijn
                new_value_total = h.total_wwijn
            elif turf_type =='rwijn':
                if h.sum_rwijn + turf_count >= 0:
                    h.sum_rwijn += Decimal(turf_count)
                    h.total_rwijn += Decimal(turf_count)
                else:
                    success_message = 'Je kan geen negatief aantal wijnflessen hebben.'
                    return HttpResponse(json.dumps({'result': success_message, 'status': 'failure'}))

                success_message = '%s heeft %s rode wijn geturft.' % (str(turf_user).capitalize(), turf_count)

                new_value = h.sum_rwijn
                new_value_total = h.total_rwijn

            h.save()

            t = Turf(turf_user_id=turf_user, turf_to=turf_user.username, turf_by=request.user, turf_count=turf_count, turf_type=turf_type)
            t.save()

            return HttpResponse(json.dumps({'result': success_message, 'status': 'success',
                                            'new_value': str(new_value), 'new_value_total': str(new_value_total)}))

        else:
            return HttpResponse(json.dumps({'result': 'Error: User not authenticated. Please log in again.', 'status': 'failure'}))


# handle turf post requests
def list_medals(request):

    if request.method == 'GET':
        if request.user.is_authenticated():

            # find medaled users
            active_users = User.objects.filter(is_active=True)
            user_medals = Housemate.objects.exclude(user__username='huis').filter(user__id__in=active_users).order_by('-sum_bier')[:3]
            medals = []

            for u in user_medals:
                if u.sum_bier > 0:
                    medals += [u.user_id]
                else:
                    medals += [0]

            return HttpResponse(json.dumps({'status': 'success', 'medals': {'gold': medals[0], 'silver': medals[1], 'bronze': medals[2]}}))

        else:
            return HttpResponse(json.dumps({'result': 'Error: User not authenticated. Please log in again.', 'status': 'failure'}))
