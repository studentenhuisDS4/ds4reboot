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
    if request.user.is_authenticated():
        if request.method == 'POST':
            # Get user and turf type from POST
                turf_user = User.objects.get(pk=user_id)
                turf_type = request.POST.get('turf_type')

                if request.POST.get('count'):

                    # validate count input
                    try:
                        turf_count = Decimal(round(Decimal(request.POST.get('count')), 2))

                    except ValueError:
                        return HttpResponse(json.dumps({'result': 'Error: Turf count must be numerical.'}))

                    if turf_type == 'bier' and not float(turf_count).is_integer():
                        return HttpResponse(json.dumps({'result': 'Error: Must turf whole beer.'}))

                    if turf_count >= 1000:
                        return HttpResponse(json.dumps({'result': 'Cannot turf more than 999 items.'}))

                else:
                    turf_count = 1

                print ('TURF | user: %s | type: %s | count: %s' % (turf_user, turf_type, turf_count))

                h = Housemate.objects.get(user_id=user_id)

                # add entry to database
                if turf_type == 'bier':
                    h.sum_bier += turf_count
                    h.total_bier += turf_count

                    # device = get_device_model()
                    # device.objects.all().send_message({'message':'my test message'})

                elif turf_type == 'wwijn':
                    h.sum_wwijn += Decimal(turf_count)
                    h.total_wwijn += Decimal(turf_count)

                elif turf_type =='rwijn':
                    h.sum_rwijn += Decimal(turf_count)
                    h.total_rwijn += Decimal(turf_count)

                h.save()

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
