from . import models
from django.shortcuts import render, redirect
from .models import ArriveLeaveGarden
from django.contrib import messages


def Arrive_DB(request, gname):
    id = request.user.id
    arrive = ArriveLeaveGarden.objects.filter(user_id=id).first()
    if arrive:
        messages.warning(request, f'you already in the {arrive.garden_name}! you cant be in two gardens at the same time')
    else:
        user = request.user
        username = request.user.username
        garden = gname
        arrive = ArriveLeaveGarden.objects.create(
            garden_name=garden,
            username=username,
            user_id=user,
        )
        arrive.save()
        messages.success(request, f'You have been checked in!')


def Leave_DB(request):
    id = request.user.id
    leave = ArriveLeaveGarden.objects.filter(user_id=id).first()
    if leave:
        leave.delete()
        messages.success(request, f'You have been checked out!')
    else:
        messages.warning(request, f'You must check in before check out!')

