from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):

    user_info = Housemate.objects.get(user_id=request.user.id)

    active_users = User.objects.filter(is_active=True)
    user_medals = Housemate.objects.filter(user__id__in=active_users).order_by('-sum_bier')[:3]

    medals = []

    for u in user_medals:
        if u.sum_bier > 0:
            medals += [u.user_id]
        else:
            medals += [0]


    context = {
        'user_info': user_info,
        'medals': medals,
    }

    return render(request, 'home/index.html', context)