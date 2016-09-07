from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


# display users index
def index(request):
    return redirect('/user/profiel/%s/' % (request.user.id))


# display profile page
def profile(request, user_id=None):
    if request.user.is_authenticated():
        if request.method == 'POST':
            return HttpResponse(json.dumps({'result': 'Profile updated.'}))

        else:
            if not user_id:
                user_id = request.user.id

            # get requested user
            profile_user = Housemate.objects.get(user_id=user_id)

            # build context object
            context = {
                'breadcrumbs': ['profiel'],
                'profile_user': profile_user
                }

            return render(request, 'user/profile.html', context)

    else:
            return render(request, 'base/login_page.html')

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
        username = request.POST['username'].lower()
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
                messages.error(request, 'Your account is disabled.')
        else:
            messages.error(request, 'Invalid login details supplied.')

        return redirect(request.META.get('HTTP_REFERER'))

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
            messages.error(request, 'Huis account is disabled.')
    else:
        messages.error(request, 'Huis account does not exist.')

    return redirect(request.META.get('HTTP_REFERER'))

