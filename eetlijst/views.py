from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render


# Create your views here.

def index(request):
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    context = {
        'user_list': user_list,
    }

    return render(request, 'eetlijst/index.html', context)