from django.shortcuts import render, redirect
import json
from . import buttons_functions
from django.contrib import messages
from . models import ArriveLeaveGarden
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


