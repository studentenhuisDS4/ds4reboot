from django.contrib.auth.models import User
from user.models import Housemate
from bierlijst.models import Turf, Boete
from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum

# import plotly.plotly as ply
# import plotly.tools as tls
# from plotly.graph_objs import *


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
def show_log(request):

    # get list of turfed items
    turf_list = Turf.objects.order_by('-turf_time')

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'turf_list': turf_list
    }

    return render(request, 'bierlijst/log.html', context)


# view for boetes including form submission
def boetes(request):

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    housemates = Housemate.objects.filter(user__id__in = active_users).exclude(display_name = 'Huis').order_by('movein_date')

    # get lists of all boetes and users with open boetes
    open_boetes = Housemate.objects.filter(boetes_open__gt = 0, user__id__in = active_users).order_by('-boetes_open')
    num_boetes = str(list(open_boetes.aggregate(Sum('boetes_open')).values())[0])
    boetes_list = Boete.objects.order_by('-created_time')

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'housemates': housemates,
        'open_boetes': open_boetes,
        'num_boetes': num_boetes,
        'boetes_list': boetes_list,
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
                return HttpResponse("Number of boetes must be between 1 and 10.")

            if note == '':
                return HttpResponse("Must add reason.")

            if user_id == 0:
                return HttpResponse("Must choose housemate.")

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
        return HttpResponse("Method must be POST.")

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

            h = Housemate.objects.get(user_id=user_id)
            h.boetes_open -= 1
            h.boetes_turfed += 1
            h.save()


            return redirect(request.META.get('HTTP_REFERER'))

        else:
            return HttpResponse("Invalid turf type.")

    else:
        return render(request, 'base/login_page.html')


# handle reset boete requests
def reset_boetes(request):

    if request.user.is_authenticated():


        Boete.objects.all().delete()

        for h in Housemate.objects.all():
            h.boetes_open = 0
            h.boetes_turfed = 0
            h.save()

        return HttpResponse("Boetes have been reset.")

    else:
        return render(request, 'base/login_page.html')


# handle turf post requests
def turf_item(request, user_id):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # validate turf type
            if 'bier' in request.POST:
                turf_type = 'bier'
            elif 'wwijn' in request.POST:
                turf_type = 'wwijn'
            elif 'rwijn' in request.POST:
                turf_type = 'rwijn'
            else:
                turf_type = 'bier'

            if request.POST.get('count'):

                # validate count input
                try:
                    turf_count = Decimal(round(Decimal(request.POST.get('count')), 2))

                except ValueError:
                    return HttpResponse("Turf count must be numerical.")

                if turf_type == 'bier' and not float(turf_count).is_integer():
                    return HttpResponse("Must turf whole beer.")

                if turf_count >= 1000:
                    return HttpResponse("Cannot turf more than 999 items.")

            else:
                turf_count = 1

            turf_user = User.objects.get(pk=user_id)

            h = Housemate.objects.get(user_id=user_id)

            # add entry to database
            if 'bier' in request.POST:
                h.sum_bier += turf_count
                h.total_bier += turf_count

            elif 'wwijn' in request.POST:
                h.sum_wwijn += Decimal(turf_count)
                h.total_wwijn += Decimal(turf_count)

            elif 'rwijn' in request.POST:
                h.sum_rwijn += Decimal(turf_count)
                h.total_rwijn += Decimal(turf_count)

            h.save()

            t = Turf(turf_user_id=turf_user, turf_to=turf_user.username, turf_by=request.user, turf_count=turf_count, turf_type=turf_type)
            t.save()

            return redirect(request.META.get('HTTP_REFERER'))

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")
