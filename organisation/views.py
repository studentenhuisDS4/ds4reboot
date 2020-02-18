from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from organisation.api.api_calendar import CalendarViewSet
from organisation.models import KeukenDienst
from user.models import Housemate


# from user.models import Housemate


def index(request):
    active_users = User.objects.filter(is_active=True).exclude(username='admin')
    active_housemates = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')

    keukendiensts = KeukenDienst.objects.filter(done=False)
    google_cal_events = get_cal_events(request)

    context = {
        'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        'active_housemates': active_housemates,
        'keukendiensts': keukendiensts,
        'google_cal_events': google_cal_events
    }

    return render(request, 'organisation/index.html', context)


def get_cal_events(request):
    google_cal_events = CalendarViewSet().list(request).data
    return google_cal_events

# @require_POST
#  def add_keukendienst(userids, date):
#     if request.user.is_authenticated:
#
#         # get data from POST
#         user_id = int(request.POST.get('housemate'))
#         note = request.POST.get('note')
#
#         if request.POST.get('count') == '':
#             count = 1
#         else:
#             count = int(request.POST.get('count'))
#
#         # validate form input
#         if count > 10 or count < 1:
#             messages.error(request, 'Number of boetes must be between 1 and 10.')
#             return redirect(request.META.get('HTTP_REFERER'))
