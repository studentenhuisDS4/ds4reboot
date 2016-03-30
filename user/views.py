from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect



# display users index
def index(request):
    return HttpResponse("Hello, world. You're at the users index.")


# display profile page
def profiel(request):

    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
    }

    return render(request, 'user/profiel.html', context)


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
