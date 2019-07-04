from django.contrib.auth.models import User
from django.shortcuts import render
# from user.models import Housemate


# Create your views here.
from user.models import Housemate


def index(request):
    active_users = User.objects.filter(is_active=True).exclude(username='admin')
    active_housemates = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'active_housemates': active_housemates,
    }

    return render(request, 'organisation/index.html', context)

#
# def Add_Keukendienst(Userid, date)
#     active_housemates = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')
#     select_housemates = active_housemates.exclude(display_name='Admin').exclude(display_name='Huis')
#     return("Hello world")
