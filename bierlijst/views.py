from django.contrib.auth.models import User
from django.shortcuts import render
from user.models import Housemate
from django.http import HttpResponse
from django.template import loader


# Create your views here.

def index(request):
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    template = loader.get_template('bierlijst/index.html')

    context = {
        'user_list': user_list,
    }

    # return HttpResponse(user_list)
    return HttpResponse(template.render(context, request))