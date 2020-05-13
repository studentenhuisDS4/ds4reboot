from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils import timezone

from eetlijst.models import Dinner, UserDinner
from organisation.views import get_cal_events
from user.models import Housemate
from game.models import SnakeHighScore

# display home page
def home_page(request):
    if request.user.is_authenticated:

        # get object for current user
        user_info = Housemate.objects.get(user_id=request.user.id)

        # load data on bierlijst medals
        active_users = User.objects.filter(is_active=True)
        user_medals = Housemate.objects.exclude(user__username='huis').filter(user__id__in=active_users).order_by(
            '-sum_bier')[:3]

        medals = []

        for u in user_medals:
            if u.sum_bier > 0:
                medals += [u.user_id]
            else:
                medals += [0]

        # load eetlijst data
        try:
            eating_with = UserDinner.objects.get(dinner_date=timezone.now(), user_id=request.user.id).count

        except UserDinner.DoesNotExist:
            eating_with = 0

        try:
            data_date = Dinner.objects.get(date=timezone.now())

            if data_date.cook:

                eetlijst_info = [Housemate.objects.get(user_id=data_date.cook.id).display_name, data_date.num_eating,
                                 eating_with, data_date.open]

            else:
                eetlijst_info = ['Geen', data_date.num_eating, eating_with, data_date.open]

        except Dinner.DoesNotExist:
            eetlijst_info = ['Geen', 0, 0, True]

        today = timezone.now()
        events = []
        try:
            events = get_cal_events(request)
        except Exception as e:
            print('!!! Cal Events failed, skipped. Exception: ', e)

        snake_highscores = None
        try:
            snake_highscores = SnakeHighScore.objects.all().order_by('-score')
        except:
            print('Some exception with fetching highscores for snake. Exception: ', e)

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'user_info': user_info,
            'eetlijst_info': eetlijst_info,
            'focus_date': str(today.year) + '-' + str(today.month) + '-' + str(today.day),
            'medals': medals,
            'google_cal_events': events,
            'snake_highscores': snake_highscores
        }

        return render(request, 'home/index.html', context)

    else:
        return render(request, 'home/index.html')


# view for relatively static contact page
def contact(request):
    # build context object
    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
    }
    return render(request, 'contact/index.html', context)
