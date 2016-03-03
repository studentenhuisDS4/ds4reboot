from django.contrib.auth.models import User
from user.models import Housemate
from bierlijst.models import Turf
from django.shortcuts import render, redirect
from django.http import HttpResponse
from decimal import Decimal
from django.db.models import Sum


# Create your views here.


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

    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'user_list': user_list,
        'totals': totals,
        'medals': medals,
    }

    return render(request, 'bierlijst/index.html', context)


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
                    turf_count = float(round(float(request.POST.get('count')), 2))

                except ValueError:
                    return HttpResponse("Turf count must be numerical.")

                if turf_type == 'bier' and not turf_count.is_integer():
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
