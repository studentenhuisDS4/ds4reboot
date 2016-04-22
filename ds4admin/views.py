from django.contrib.auth.models import User
from user.models import Housemate
from eetlijst.models import HOLog
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils import timezone


# view for ds4 admin page
def index(request):

    # get list of active users sorted by move-in date
    active_users = User.objects.filter(is_active=True)
    housemates = Housemate.objects.filter(user__id__in = active_users).exclude(display_name = 'Huis').order_by('movein_date')

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'housemates': housemates,
        }

    return render(request, 'ds4admin/index.html', context)


# handle remove housemate post requests
def remove_housemate(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            remove_id = int(request.POST.get('housemate'))

            if not remove_id:
                return HttpResponse("Must specify housemate to be removed.")

            else:
                # update housemate object
                h = Housemate.objects.get(user_id=remove_id)
                h.moveout_set = False
                h.moveout_date = timezone.now()
                remaining_balance = h.balance
                # h.balance = 0
                h.save()

                u = h.user
                u.is_active = False
                u.save()

                #update housemate objects for other users
                huis = Housemate.objects.get(display_name='Huis')
                amount = -1 * remaining_balance

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
                ho = HOLog(user=h.user, amount=remaining_balance, note='Verhuizen')
                ho.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        return HttpResponse("Method must be POST.")

    return redirect(request.META.get('HTTP_REFERER'))