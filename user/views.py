from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect



# display users index
def index(request):
    return redirect('/user/profiel/%s/' % (request.user.id))


# display profile page
def profile(request, user_id=None):

    if user_id:

        # get list of active users sorted by move-in date
        active_users = User.objects.filter(is_active=True)
        housemates = Housemate.objects.filter(user__id__in = active_users).exclude(display_name = 'Huis').order_by('movein_date')

        # build context object
        context = {
            'breadcrumbs': ['profiel'],
            'housemates': housemates,
            }

        return render(request, 'user/profile.html', context)

    else:
        return redirect('/user/profiel/%s/' % (request.user.id))


# display settings page
def settings(request):

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
    }

    return render(request, 'user/settings.html', context)


# handle requests from login form
def login_user(request):

    if request.method == 'POST':

        # get credentials from post and authenticate user
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                if '/user/login' in request.META.get('HTTP_REFERER'):
                    return redirect('/')
                else:
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:


        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        }

        return render(request, 'base/login_page.html', context)


# handle logout requests
def logout_user(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

# login as 'huis'
def login_huis(request):
    logout(request)

    user = authenticate(username='huis', password='pass')

    if user:
        if user.is_active:

            login(request, user)
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            return HttpResponse("Your account is disabled.")
    else:
        return HttpResponse("Invalid login details supplied.")
