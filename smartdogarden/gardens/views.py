from django.shortcuts import render
import json
# Create your views here.


def view_gardens(request):
    json_data = open('data_from_b7_open_data/dog-gardens.json')
    data1 = json.load(json_data)  # deserialises it
    json_data.close()
    return render(request, 'gardens/base.html', {"list": data1})
