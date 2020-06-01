from django.shortcuts import render, redirect
import json
from . import buttons_functions
from django.contrib import messages
from .models import ArriveLeaveGarden, ReportOnHazard, HazardReports
from .forms import HazardReportForm, UpdateHazardReportStatus


# Create your views here.


def view_gardens(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/view_gardens.html', {"list": data1})


def view_arrive_or_leave(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/arrive_or_leave.html', {"list": data1})


def view_test(request):
    gname = request.GET['gname']
    if gname == "Leave":
        buttons_functions.Leave_DB(request)
        return render(request, 'gardens/arrive_or_leave.html')
    else:
        buttons_functions.Arrive_DB(request, gname)
        return render(request, 'gardens/arrive_or_leave.html')


def view_who_in_garden(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/view_who_in_garden.html', {"list": data1})


def view_users_in_garden(request):
    gname = request.GET['gname']
    users = ArriveLeaveGarden.objects.all()
    good = users.filter(garden_name=gname)

    return render(request, 'gardens/view_users_in_garden.html', {"list": good})


def view_hazard_report(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/hazard_report.html', {"list": data1})


def report_on_hazard(request):
    # if request.method == 'POST':
    gname = request.GET['gname']
    form = HazardReportForm(request.POST)
    if form.is_valid():
        username = request.user.username
        user = request.user
        new_hazard = ReportOnHazard.objects.create(
            report_title=form.cleaned_data['report_title'],
            report_text=form.cleaned_data['report_text'],
            reporter_id=user,
            reporter_user_name=username,
            garden_name=gname,
        )
        new_hazard.save()
        messages.success(request, f'Hazard report created successfully!')
        return redirect('view_hazard_report')
    else:
        form = HazardReportForm()

    return render(request, 'gardens/report_on_hazard.html', {'form': form})


def all_hazard_report(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json', encoding="utf8")
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/all_hazard_report.html', {"list": data1})


def view_all_hazard_report(request):
    gname = request.GET['gname']
    users = HazardReports.objects.all()
    good = users.filter(garden_name=gname)
    return render(request, 'gardens/view_all_hazard_report.html', {"list": good})


def admin_view_reports(request):
    reports = HazardReports.objects.all()
    return render(request, 'gardens/view_all_hazard_report.html', {"list": reports})


def admin_view_user_hazard_report_to_approve(request):
    reports_to_approve = ReportOnHazard.objects.all()
    return render(request, 'gardens/view_all_hazard_reports_to_approve.html', {"list": reports_to_approve})


def admin_approve_hazard_report(request):
    report_id = request.GET['report_id']
    the_report = ReportOnHazard.objects.filter(id=report_id).first()
    new_hazard = HazardReports.objects.create(
        report_title=the_report.report_title,
        report_text=the_report.report_text,
        reporter_id=the_report.reporter_id,
        reporter_user_name=the_report.reporter_user_name,
        garden_name=the_report.garden_name,
    )
    new_hazard.save()
    if new_hazard:
        messages.success(request, f'Hazard report approved and created successfully!')
        the_report.delete()
    else:
        messages.warning(request, f'Hazard report isnt approved successfully!')
    return redirect('view_reports_requests')


def admin_reject_hazard_report(request):
    report_id = request.GET['report_id']
    the_report = ReportOnHazard.objects.filter(id=report_id).first()
    the_report.delete()
    the_report = ReportOnHazard.objects.filter(id=report_id).first()
    if the_report:
        messages.warning(request, f'Hazard report isnt rejected successfully!')
    else:
        messages.success(request, f'Hazard report rejected and deleted successfully!')
    return redirect('view_reports_requests')


def update_hazard_report_status(request):
    report_id = request.GET['report_id']
    the_report = HazardReports.objects.filter(id=report_id).first()
    form = UpdateHazardReportStatus(request.POST)
    if form.is_valid():
        the_report.report_status = form.cleaned_data['report_status']
        the_report.save()
        messages.success(request, f'Hazard report status changed successfully!')
        return redirect('admin_view_reports')
    else:
        form = UpdateHazardReportStatus()

    return render(request, 'gardens/update_hazard_report_status.html', {'form': form})