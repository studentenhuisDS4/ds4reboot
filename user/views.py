from django.contrib.auth.models import User
from user.models import Housemate
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
import json


# display users index
def index(request):
    return redirect('/user/profiel/%s/' % request.user.id)


# display profile page
def profile(request, user_id=None):
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                if request.POST.get("profile-edit-type", "") == "profile":

                    # Assume client side validation has succeeded
                    email = request.POST.get("email", "")
                    cellphone = request.POST.get("cellphone", "")
                    parentphone = request.POST.get("parentphone", "")
                    diet = request.POST.get("diet", "")
                    room_number = request.POST.get("room-number", "")

                    # Define user to be changed
                    if request.user.id == user_id or user_id == None:
                        user = request.user
                    else:
                        user = User.objects.get(id=user_id)
                        if user is None:
                            messages.error(request, 'Gebruiker-profiel is niet bekend.')

                    if email == "" and user.email != "":
                        messages.warning(request, 'Email verwijderd.')
                    if cellphone == "" and user.housemate.cell_phone != "":
                        messages.warning(request, 'Telefoonnummer verwijderd.')
                    if parentphone == "" and user.housemate.parent_phone != "":
                        messages.warning(request, 'Telefoonnummer ouders verwijderd.')
                    if diet == "" and user.housemate.diet != "":
                        messages.warning(request, 'Diet verwijderd.')
                    if room_number == "" and not user.is_active and user.housemate.room_number != "":
                        messages.warning(request, 'Room number deleted for inactive user.')

                    user.email = email
                    user.housemate.cell_phone = cellphone
                    user.housemate.parent_phone = parentphone
                    user.housemate.diet = diet
                    if room_number != "" and user.is_active:
                        user.housemate.room_number = room_number
                    elif room_number == "" and not user.is_active:
                        user.housemate.room_number = None
                    else:
                        messages.warning(request, 'Can\'t delete room number when user is still active.')
                    user.housemate.save()
                    user.save()

                    messages.success(request, 'Profielaanpassing voor ' +
                                     user.first_name + ' geslaagd.')

                elif request.POST.get("profile-edit-type", "") == "password":
                    current_pass = request.POST.get("current-pass", "")
                    new_pass = request.POST.get("new-pass", "")
                    verify_pass = request.POST.get("verify-pass", "")

                    if len(current_pass) == 0 and len(current_pass) > 5:
                        messages.error(request, 'Huidig wachtwoord is niet lang genoeg of niet gegeven.')
                    elif len(new_pass) == 0 and len(new_pass) > 5:
                        messages.error(request, 'Nieuw wachtwoord is niet lang genoeg of niet gegeven.')
                    elif len(verify_pass) == 0 and len(verify_pass) > 5:
                        messages.error(request, 'Nieuw (herhaald) wachtwoord is niet lang genoeg of niet gegeven.')
                    elif new_pass != verify_pass:
                        messages.error(request, 'Nieuw (herhaald) wachtwoord is niet goed herhaald.')
                    elif current_pass == new_pass or current_pass == verify_pass:
                        messages.error(request,
                                       'Nieuw, of herhaald wachtwoord is hetzelfde als het huidige wachtwoord.')
                    else:
                        # Define user to be changed
                        if request.user.id == user_id or user_id is None:
                            user = request.user
                        else:
                            user = User.objects.get(id=user_id)

                        if user is not None:
                            # Authenticate current password
                            user_auth = authenticate(username=user.username, password=current_pass)
                            if user_auth is not None:
                                user_auth.set_password(new_pass)
                                messages.success(request, 'Wachtwoord succesvol aangepast voor ' +
                                                 user_auth.first_name + '.')
                                user_auth.save()
                            else:
                                messages.error(request, 'Het huidige wachtwoord voor ' +
                                               user.first_name + ' is onjuist.')
                        else:
                            messages.error(request, 'Gebruiker-profiel is niet bekend.')

                else:
                    messages.error(request, 'Wrong profile editing type or unknown editing request.')
            except Exception as e:
                messages.error(request, 'Het formulier kon niet succesvol gevalideerd worden. ' + str(e))

            if not user_id:
                user_id = request.user.id

            # get requested user
            profile_user = Housemate.objects.get(user_id=user_id)

            # build context object
            context = {
                'breadcrumbs': ['profiel'],
                'profile_user': profile_user,
            }

            if request.user.is_superuser:
                active_users = Housemate.objects.exclude(display_name='Huis').exclude(display_name='Admin') \
                    .exclude(user__is_active=False).order_by('movein_date')

                context['active_users'] = active_users
                context['rooms'] = active_users

            return render(request, 'user/profile.html', context)
            # return HttpResponse(json.dumps({'result': 'Profile updated.'}))

        else:
            if not user_id:
                user_id = request.user.id

            # get requested user
            profile_user = Housemate.objects.get(user_id=user_id)
            active_users = Housemate.objects.exclude(display_name='Huis').exclude(display_name='Admin') \
                .exclude(user__is_active=False).order_by('movein_date')

            rooms = dict()
            duplicates = dict()
            for user in active_users:
                if len({k: v for k, v in rooms.items() if v.room_number == user.room_number}) == 0:
                    rooms[user.user_id] = user
                else:
                    duplicates[user.user_id] = user

            # build context object
            context = {
                'breadcrumbs': ['profiel'],
                'profile_user': profile_user,
                'active_users': active_users,
                'duplicate_rooms': duplicates,
                'rooms': rooms
            }

            return render(request, 'user/profile.html', context)
    else:
        return render(request, 'base/login_page.html')


# handle requests from login form
def login_user(request):
    if request.method == 'POST':

        # get credentials from post and authenticate user
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if not user:
            user = authenticate(username=username.lower(), password=password)

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
