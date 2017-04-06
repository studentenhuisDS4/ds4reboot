from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.core.files import File
from thesau.forms import MutationsUploadForm
from thesau.models import Report, BoetesReport, UserReport, MutationsFile, MutationsParsed
from user.models import Housemate
from decimal import Decimal
from openpyxl import Workbook
import datetime
import mt940


# view for thesau page
def index(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        report_list = Report.objects.all()

        # Get active and last closed report
        current_open_report = get_open_report(request.user)
        latest_report = get_latest_closed_report()

        # If no closed HR report exist, assume creation day as last HR end
        if latest_report is None:
            last_HR_date = current_open_report.report_date
            HR_day_difference = (datetime.date.today() - last_HR_date).days + 1
        else:
            last_HR_date = latest_report.report_date
            HR_day_difference = (datetime.date.today() - latest_report.report_date).days + 1

        # Stats for result bar
        muts_applied = MutationsParsed.objects.filter(report=current_open_report, applied=True)

        if len(muts_applied) > 0:
            date_begin = muts_applied.earliest('mutation_date').mutation_date
            date_end = muts_applied.latest('mutation_date').mutation_date
            mut_begin = MutationsParsed.objects.filter(mutation_date=date_begin).earliest('id')
            mut_end = MutationsParsed.objects.filter(mutation_date=date_end).latest('id')
            bal_begin = mut_begin.start_balance
            bal_end = mut_end.end_balance
        else:
            date_begin = None
            date_end = None
            bal_begin = '?'
            bal_end = '?'

        total_used_mutations = len(muts_applied)

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'report_list': report_list,
            'last_HR_date': last_HR_date,
            'current_date': timezone.now().date,
            'duration_HR': HR_day_difference,
            'muts_used': total_used_mutations,
            'balance_start': bal_begin,
            'balance_end': bal_end,
            'date_begin': date_begin,
            'date_end': date_end,
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

    # Save contents, so they are available as ContentType
    path = 'media/hr_reports/HR_temp.xlsx'
    wb.save(path)

    f = open(path, 'rb')
    xlsx_file = File(f)

    # Relocate file so it is available in the database
    r_file_name = 'HR_%s_%s.xlsx' % (date.year, months[date.month])

    # get report entry in database or create it
    r = get_open_report(request.user)
    r.report_name = 'HR %s %s' % (months[date.month], date.year)
    r.report_date = date
    r.report_file.save(r_file_name, xlsx_file)
    r.report_closed = True
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


def bank_mutations_upload(request, form, current_open_report):

    # Handle file upload
    try:
        if form.is_valid():
            # form_data = form.cleaned_data

            # Fill data for to process file upload
            MutFile = MutationsFile(sta_file=request.FILES['sta_file'],
                                    # description=form_data['description'],
                                    report=current_open_report,
                                    upload_user=request.user,
                                    applied=True)
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

                T_sum_amounts_pre = Decimal(0.00)
                T_sum_amounts_post = Decimal(0.00)
                for t in T:
                    amount = t.data['amount'].amount
                    T_sum_amounts_post += amount

                # Generate open balance from close balance - difference
                open_amount = mt940.models.\
                    Amount(str(bal2dec(T_close_bal) - T_sum_amounts_post),
                           status='C',
                           currency=T_close_bal.amount.currency)
                T_open_bal = mt940.models.\
                    Balance(amount=open_amount,
                            status='C',
                            date=T[0].data['entry_date'])

                # print('Opening balance: ' + str(T_open_bal))
                # print('Closing balance: ' + str(T_close_bal))

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

                    # Extract source and dest. IBAN
                    t_details = t.data['transaction_details']
                    t_IBAN = find_between(t_details, '/IBAN/', '/')
                    t_NAME = find_between(t_details, '/NAME/', '/')
                    t_INFO = find_between(t_details, '/REMI/', '/')

                    # No parsing ocurred, check for BEA pin transaction
                    if t_IBAN == "":
                        try:
                            t_IBAN = 'NL89ABNA0479039860'
                            t_INFO = t_details
                            t_NAME = "#!Could not parse name!#"
                            if t_details.find('BEA') != -1 and t_details.find('NR') != -1:
                                pin_details = t_details.split("   ")
                                if pin_details[0] == 'BEA':
                                    pin_split = pin_details[2].split(' ')
                                    pin_time = pin_split[0]
                                    pin_info = find_between(pin_details[2], pin_time + ' ', 'PAS')
                                    t_NAME = 'PIN'
                                    t_INFO = pin_info + ' @' + pin_time + ' ' + pin_details[1]
                            else:
                                # Test if ABN string is found, then bank transaction
                                if t_details.find('ABN AMRO BANK N.V.') != -1:
                                    t_INFO = "Interne bank transactie"
                                    t_NAME = "ABN AMRO BANK N.V."
                        except Exception as e:
                            print('Problem: ' + t_details + ' Exc: ' + str(e))

                    # Check if there are duplicate entries
                    # TODO check for transactions outside HR period
                    # (check previous HR report date and check with todays date)

                    mut_duplicates = MutationsParsed.objects. \
                        filter(mutation_date=t_date,
                               source_IBAN=t_IBAN,
                               dest_IBAN='NL89ABNA0479039860',
                               start_balance=t_start_bal,
                               end_balance=t_end_bal)

                    # Skip duplicate mutation
                    if len(mut_duplicates) > 0:
                        num_duplicate_mut += 1
                        continue
                    else:
                        MutParsed = MutationsParsed(report=current_open_report,
                                                    start_balance=t_start_bal,
                                                    end_balance=t_end_bal,
                                                    source_IBAN=t_IBAN,
                                                    dest_IBAN='NL89ABNA0479039860',
                                                    source_name=t_NAME,
                                                    mutation_info=t_INFO,
                                                    mutation_date=t_date,
                                                    mutation_file=MutFile,
                                                    applied=True)
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

            return HttpResponseRedirect("/thesau/bank_mutations/")
    except Exception as e:
        messages.error(request, 'File uploading (partially) failed.')


def bank_mutations(request):

    if request.user.groups.filter(name='thesau').exists() or request.user.is_superuser:

        # Get active and last closed report
        current_open_report = get_open_report(request.user)
        latest_report = get_latest_closed_report()
        if latest_report is None:
            last_HR_date = current_open_report.report_date
            HR_day_difference = (datetime.date.today() - current_open_report.report_date).days + 1
        else:
            last_HR_date = latest_report.report_date
            HR_day_difference = (datetime.date.today() - latest_report.report_date).days + 1

        if request.method == 'POST':
            form = MutationsUploadForm(request.POST, request.FILES)
            return bank_mutations_upload(request, form, current_open_report)
        else:
            # A empty form which is loaded in background DOM
            form = MutationsUploadForm()

        mut_files = MutationsFile.objects.filter(report=current_open_report)
        used_mut_files = mut_files.exclude(applied=False)
        muts_applied = MutationsParsed.objects.filter(report=current_open_report, applied=True)

        if len(muts_applied) > 0:
            date_begin = muts_applied.earliest('mutation_date').mutation_date
            date_end = muts_applied.latest('mutation_date').mutation_date
            mut_begin = MutationsParsed.objects.filter(mutation_date=date_begin).earliest('id')
            mut_end = MutationsParsed.objects.filter(mutation_date=date_end).latest('id')
            bal_begin = mut_begin.start_balance
            bal_end = mut_end.end_balance
        else:
            date_begin = None
            date_end = None
            bal_begin = '?'
            bal_end = '?'

        # build up warnings and errors
        warnings = dict()
        errors = dict()

        total_used_mutations = 0
        for used_mut_file in used_mut_files:
            total_used_mutations += used_mut_file.num_mutations
            if used_mut_file.num_duplicates != 0:
                try:
                    warnings['overlap_files'] += 1
                except:
                    warnings['overlap_files'] = 1
            if used_mut_file.closing_balance < Decimal(0.00):
                warnings['negative_balance'] = True
            if last_HR_date is not None:
                if used_mut_file.opening_date < last_HR_date:
                    warnings['overlap_prev_hr'] = True

        if len(mut_files) == 0:
            errors['no_uploaded_files'] = True
        elif len(used_mut_files) == 0:
            errors['no_applied_files'] = True

        # build context object
        context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
            'last_HR_date': last_HR_date,
            'current_date': timezone.now().date,
            'duration_HR': HR_day_difference,
            'mut_files': mut_files.order_by('id'),
            'muts_used': total_used_mutations,
            'muts_applied': muts_applied.order_by('mutation_date'),
            'balance_start': bal_begin,
            'balance_end': bal_end,
            'date_begin': date_begin,
            'date_end': date_end,
            'form': form,
            'warnings': warnings,
            'errors': errors,
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


# An extended version of get_or_create with latest filter to get last closed report
def get_latest_closed_report():

    # Make sure an open report is generated
    closed_reports = Report.objects.filter(report_closed=True)
    if len(closed_reports):
        return closed_reports.latest(field_name='report_date')
    else:
        return None


def get_open_report(user):
    # There must be at least one open reports
    open_reports = Report.objects.exclude(report_closed=True)
    if len(open_reports) == 0:
        open_report = Report(report_user=user,
                             report_closed=False)
        open_report.save()
        return open_report
    elif len(open_reports) == 1:
        return open_reports[0]
    else:
        # There may not be more than one open report
        raise AssertionError


def bal2dec(bal):
    return bal.amount.amount


def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""