from django.shortcuts import render, redirect
import json
from . import buttons_functions
from django.contrib import messages
from .models import ArriveLeaveGarden, ReportOnHazard
from .forms import HazardReportForm


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
    users = ReportOnHazard.objects.all()
    good = users.filter(garden_name=gname)
    return render(request, 'gardens/view_all_hazard_report.html', {"list": good})


def admin_view_reports(request):
    reports = ReportOnHazard.objects.all()
    return render(request, 'gardens/view_all_hazard_report.html', {"list": reports})
