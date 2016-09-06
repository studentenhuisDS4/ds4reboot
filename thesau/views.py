from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils import timezone
from thesau.models import Report, BoetesReport, UserReport
from user.models import Housemate
from django.contrib import messages
from decimal import Decimal
from openpyxl import Workbook

# view for thesau page
def index(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        # get reports archive
        report_list = Report.objects.all()

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'report_list': report_list,
            }
        return render(request, 'thesau/index.html', context)

    else:
        messages.error(request, 'Only accessible to thesaus and admins.')
        return redirect('/')

# view for HR page
def hr(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        # generate necessary user lists
        active_users = User.objects.filter(is_active=True)
        user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')
        moveout_list = Housemate.objects.filter(moveout_set=0).order_by('moveout_date')

        # calculate turf totals
        totals = [str(list(user_list.aggregate(Sum('sum_bier')).values())[0]),
                  str(list(user_list.aggregate(Sum('sum_wwijn')).values())[0]),
                  str(list(user_list.aggregate(Sum('sum_rwijn')).values())[0]),
                  str(list(user_list.aggregate(Sum('boetes_geturfd')).values())[0])]

        # get boete counts
        # boetes_w = BoetesReport.objects.get_or_create(type='w', defaults={'boete_count': 0})
        # boetes_r = BoetesReport.objects.get_or_create(type='r', defaults={'boete_count': 0})

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'user_list': user_list,
            'moveout_list': moveout_list,
            'boetes': [BoetesReport.objects.get(type='w').boete_count, BoetesReport.objects.get(type='r').boete_count],
            'totals': totals,
            }

        return render(request, 'thesau/hr.html', context)

    else:
        messages.error(request, 'Only accessible to thesaus and admins.')
        return redirect('/')


# handle add item post requests
def add_item(request):

    if request.method == 'POST':
        if request.user.is_authenticated():

            # get data from POST
            item_type = request.POST.get('type')
            item_note = request.POST.get('note')
            item_amount = Decimal(round(Decimal(request.POST.get('amount')),2))

            if item_type == '':
                item_type = 'Overig'

            if item_note == '':
                return HttpResponse("Must add note.")
                messages.error(request, '')
                return redirect(request.META.get('HTTP_REFERER'))

            if request.user.id == 0:
                return HttpResponse("Must use non-house account.")
                messages.error(request, '')
                return redirect(request.META.get('HTTP_REFERER'))

            # add entry to boete table
            i = ItemsReport(submit_user=request.user, type=item_type, amount=item_amount, note=item_note)
            i.save()

        else:
            return render(request, 'base/login_page.html')

    else:
        messages.error(request, 'Method must be POST.')

    return redirect(request.META.get('HTTP_REFERER'))


# generate XLSX file and commit changes
def submit_hr(request):

    # generate necessary user lists
    active_users = User.objects.filter(is_active=True)
    user_list = Housemate.objects.filter(user__id__in=active_users).order_by('movein_date')
    moveout_list = Housemate.objects.filter(moveout_set=0).order_by('moveout_date')

    # calculate turf totals
    totals = [list(user_list.aggregate(Sum('sum_bier')).values())[0],
              list(user_list.aggregate(Sum('sum_wwijn')).values())[0],
              list(user_list.aggregate(Sum('sum_rwijn')).values())[0],
              list(user_list.aggregate(Sum('boetes_geturfd')).values())[0]]

    # get boete counts
    boetes_rwijn = BoetesReport.objects.get(type='r')
    boetes_wwijn = BoetesReport.objects.get(type='w')

    # make workbook and select active worksheet
    wb = Workbook()
    ws1 = wb.active

    ws1.title = 'Bierlijst'
    ws1.append(['Naam', 'Bier', 'W. Wijn', 'R. Wijn', 'Boetes'])

    for u in user_list:
        ws1.append([u.display_name, u.sum_bier, u.sum_wwijn, u.sum_rwijn, u.boetes_geturfd])

    ws1.append(['Totaal', totals[0], totals[1], totals[2], totals[3]])

    # create secondary worksheets
    ws2 = wb.create_sheet()
    ws2.title ='Geturfd Boetes'

    ws2.append(['W. Wijn', 'R. Wijn'])
    ws2.append([boetes_wwijn.boete_count, boetes_rwijn.boete_count])

    # reset boetes count
    boetes_wwijn.boete_count = 0
    boetes_rwijn.boete_count = 0
    boetes_wwijn.save()
    boetes_rwijn.save()

    if moveout_list:
        ws3 = wb.create_sheet()

        ws3.title ='Eetlijst Saldo'
        ws3.sheet_properties.tabColor = "FB29B4"
        ws3.append(['Naam', 'Verhuizing datum', 'Saldo over'])

        for u in moveout_list:
            ws3.append([u.display_name, u.moveout_date, u.balance])

    # save the file
    date = timezone.now()
    months = {1: 'januari', 2: 'februari', 3: 'maart', 4: 'april', 5: 'mei', 6: 'juni', 7: 'juli', 8: 'augustus', 9: 'september', 10: 'oktober', 11: 'november', 12: 'december'}

    path = 'static/hr_reports/HR_%s_%s.xlsx' % (date.year, months[date.month])

    wb.save(path)

    # create report entry in database
    r = Report(report_user=request.user, report_name='HR %s %s' % (months[date.month], date.year), report_date=date, report_path=path)
    r.save()

    report_users = user_list | moveout_list
    for u in report_users:
        if u in moveout_list:
            open_balance = u.balance
            u.moveout_set = True

        else:
            open_balance = 0

        ur = UserReport(user=u.user, report=Report.objects.latest('id'), hr_bier=u.sum_bier, hr_wwijn=u.sum_wwijn, hr_rwijn=u.sum_rwijn, hr_boetes=u.boetes_geturfd, eetlijst_balance=open_balance)
        ur.save()

        u.sum_bier = 0
        u. sum_wwijn = 0
        u.sum_rwijn = 0
        u.boetes_geturfd = 0

        u.save()

    return redirect('/thesau/')