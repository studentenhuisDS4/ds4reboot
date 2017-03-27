from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from thesau.forms import MutationsUploadForm
from django.utils import timezone
from thesau.models import Report, BoetesReport, UserReport, MutationsFile, MutationsParsed
from user.models import Housemate
from django.contrib import messages
from decimal import Decimal
from openpyxl import Workbook
import datetime
import mt940, pprint

# view for thesau page
def index(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        # get reports archive
        report_list = Report.objects.all()
        latest_report = get_latest_report(request.user)
        HR_day_difference = (datetime.date.today() - latest_report.report_date).days + 1

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'report_list': report_list,
            'latest_HR': latest_report,
            'current_date': timezone.now().date,
            'duration_HR': HR_day_difference
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
        boetes_w = BoetesReport.objects.get_or_create(type='w', defaults={'boete_count': 0})
        boetes_r = BoetesReport.objects.get_or_create(type='r', defaults={'boete_count': 0})

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'user_list': user_list,
            'moveout_list': moveout_list,
            'boetes': [boetes_w[0].boete_count, boetes_r[0].boete_count],
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
                messages.error(request, 'Must add note.')
                return redirect(request.META.get('HTTP_REFERER'))

            if request.user.id == 0:
                messages.error(request, 'Must use non-house account.')
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
    boetes_rwijn = BoetesReport.objects.get_or_create(type='r', defaults={'boete_count': 0})
    boetes_wwijn = BoetesReport.objects.get_or_create(type='w', defaults={'boete_count': 0})

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
    ws2.append([boetes_wwijn[0].boete_count, boetes_rwijn[0].boete_count])

    # reset boetes count
    boetes_wwijn[0].boete_count = 0
    boetes_rwijn[0].boete_count = 0
    boetes_wwijn[0].save()
    boetes_rwijn[0].save()

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

    # get report entry in database or create it
    r = get_latest_report(request.user)
    r.report_name = 'HR %s %s' % (months[date.month], date.year)
    r.report_date = date
    r.report_path = path
    r.report_closed = True
    # r = Report(report_user=request.user, report_name='HR %s %s' % (months[date.month], date.year), report_date=date, report_path=path)
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


def bank_mutations_change(request, type, file_id):
    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:
        if request.method == 'GET':
            try:
                MutFile = MutationsFile.objects.get(id=file_id)
                ParsedMuts = MutationsParsed.objects.filter(mutation_file=MutFile)
                if type == 'select':
                    MutFile.applied = True
                    ParsedMuts.update(applied=True)
                    MutFile.save()
                    messages.success(request, 'Mutation file is applied.')
                elif type == 'unselect':
                    MutFile.applied = False
                    ParsedMuts.update(applied=False)
                    MutFile.save()
                    messages.success(request, 'Mutation file is unapplied.')
                elif type == 'delete':
                    try:
                        ParsedMuts.delete()
                        MutFile.delete()
                        messages.warning(request, 'Mutation file and associated mutations are deleted.')
                    except Exception as e:
                        messages.error(request, 'Could not delete mutation file: ' + str(e))
            except Exception as e:
                messages.error(request, 'Mutation file could not be altered.' + str(e))

            return redirect('/thesau/bank_mutations/')
        else:
            messages.error(request, 'Method must be GET.')
    else:
        messages.error(request, 'Only accessible to thesaus and admins.')

    return redirect('/')


def bank_mutations(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        form = MutationsUploadForm(request.POST, request.FILES)  # A empty, unbound form
        latest_report = get_latest_report(request.user)

        # Handle file upload
        if request.method == 'POST':
            try:
                if form.is_valid():
                    form_data = form.cleaned_data

                    # Fill data for to process file upload
                    MutFile = MutationsFile(sta_file=request.FILES['sta_file'],
                                            description=form_data['description'],
                                            report=latest_report,
                                            upload_user=request.user)
                    # Process the file and make sure the path is defined
                    MutFile.save()

                    # Process and parse data of MT940 file
                    try:
                        # Parse transactions
                        T = parse_transactions(MutFile.sta_file.path)
                        T_close_date = T[-1].data['entry_date']
                        T_open_date = T[0].data['entry_date']
                        MutFile.opening_date = T_open_date
                        MutFile.closing_date = T_close_date
                        T_close_bal = T.data['final_closing_balance']

                        T_sum_amounts_post = Decimal(0.00)
                        for t in T:
                            amount = t.data['amount'].amount
                            T_sum_amounts_post += amount

                        # Generate open balance from close balance - difference
                        open_amount = mt940.models.Amount(str(bal2dec(T_close_bal) - T_sum_amounts_post),
                                                          status='C',
                                                          currency=T_close_bal.amount.currency)
                        T_open_bal = mt940.models.Balance(amount=open_amount,
                                                          status='C',
                                                          date=T[0].data['entry_date'])

                        print('Opening balance: ' + str(T_open_bal))
                        print('Closing balance: ' + str(T_close_bal))

                        # Initialize variables
                        T_sum_amounts_post = Decimal(0.00)
                        num_duplicate_mut = 0

                        # Loop through transactions
                        for t in T:
                            amount = t.data['amount'].amount
                            t_date = t.data['entry_date']
                            T_sum_amounts_pre = T_sum_amounts_post
                            T_sum_amounts_post += amount

                            t_start_bal = T_sum_amounts_pre + bal2dec(T_open_bal)
                            t_end_bal = T_sum_amounts_post + bal2dec(T_open_bal)

                            # Check if there are duplicate entries
                            # TODO check for transactions outside HR period
                            # (check previous HR report date and check with todays date)

                            # TODO improve duplicate checking
                            # find IBAN source and destination if possible
                            mut_duplicates = MutationsParsed.objects.filter(mutation_date=t_date,
                                                                            source_IBAN='NL25INGB0002744573',
                                                                            dest_IBAN='NL25INGB0002744573',
                                                                            start_balance=t_start_bal,
                                                                            end_balance=t_end_bal)
                            # Skip duplicate mutation
                            if len(mut_duplicates) > 0:
                                num_duplicate_mut += 1
                                continue
                            else:
                                MutParsed = MutationsParsed(report=latest_report,
                                                start_balance=t_start_bal,
                                                end_balance=t_end_bal,
                                                source_IBAN='NL25INGB0002744573',
                                                dest_IBAN='NL25INGB0002744573',
                                                mutation_date=t_date,
                                                mutation_file=MutFile,
                                                applied=False)
                                MutParsed.save()

                        MutFile.opening_balance = bal2dec(T_open_bal)
                        MutFile.closing_balance = bal2dec(T_close_bal)
                        MutFile.num_mutations = len(T) - num_duplicate_mut
                        MutFile.num_duplicates = num_duplicate_mut

                        if MutFile.num_mutations == 0:
                            MutFile.delete()
                            messages.warning(request, 'Bestand bevatte geen nieuwe mutaties en is genegeerd.')
                        else:
                            MutFile.save()
                            messages.success(request, 'Bestand ge-upload.')
                    except Exception as e:
                        print(str(e))
                        messages.error(request, 'File processing (partially) failed.')
                        MutFile.delete()

                        # Count transactions and duplications
            except Exception as e:
                messages.error(request, 'File uploading (partially) failed.')

        # get reports archive
        HR_day_difference = (datetime.date.today() - latest_report.report_date).days + 1
        mut_files = MutationsFile.objects.filter(report=latest_report)
        used_mut_files = mut_files.exclude(applied=False)
        applied_muts = MutationsParsed.objects.filter(report=latest_report, applied=True)

        total_used_mutations = 0
        for used_mut_file in used_mut_files:
            total_used_mutations += used_mut_file.num_mutations

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'latest_HR': latest_report,
            'current_date': timezone.now().date,
            'duration_HR': HR_day_difference,
            'mut_files': mut_files.order_by('id'),
            'applied_muts': applied_muts,
            'num_used_mut': total_used_mutations,
            'form': form
        }

        # Render list page with the documents and the form
        return render(request, 'thesau/bank_mutations.html', context)
    else:
        messages.error(request, 'Only accessible to thesaus and admins.')
        return redirect('/')

def parse_transactions(file):
    with open(file) as f:
        data = f.read()

    t_proc = mt940.models.Transactions.DEFAULT_PROCESSORS

    transactions = mt940.models.Transactions(processors=t_proc)
    transactions.parse(data)

    return transactions

# An extended version of get_or_create with latest filter
def get_latest_report(user):

    if len(Report.objects.exclude(report_closed=True)) == 0:
        latest_report = Report(report_user=user,
                               report_date=datetime.date.today(),
                               report_closed=False)
        latest_report.save()
    else:
        latest_report = Report.objects.latest(field_name='report_date')

    return latest_report

def bal2dec(bal):
    return bal.amount.amount
