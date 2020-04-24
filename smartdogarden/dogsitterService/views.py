from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from dogsitterService.forms import ActivityTimeDogSitterForm
from dogsitterService.models import ActivityTimeDogSitter


def activity_time(request):
    id = request.user.id
    allactivities = ActivityTimeDogSitter.objects.filter(user_id=id)
    return render(request, 'dogsitterService/activity_time.html', {"list": allactivities})


def add_activity_time(request):
    if request.method == 'POST':
        form = ActivityTimeDogSitterForm(request.POST)
        if form.is_valid():
            user = request.user
            username = request.user.username
            id = request.user.id
            allactivities = ActivityTimeDogSitter.objects.all()
            myactivities = allactivities.filter(user_id=id)
            for i in myactivities:
                if i.activity_date == form.cleaned_data['activity_date'] :
                    print('helloooooo')
                    if form.cleaned_data['activity_start'] > i.activity_start and form.cleaned_data['activity_start'] < i.activity_end  or form.cleaned_data['activity_end'] > i.activity_start and form.cleaned_data['activity_end'] < i.activity_end:
                        messages.warning(request, f'Activity time is overlapped!')
                        return redirect('add_activity_time')
                    if form.cleaned_data['activity_start'] == i.activity_start or form.cleaned_data['activity_end'] == i.activity_end:
                        messages.warning(request, f'Activity time already exists!')
                        return redirect('add_activity_time')
            activity_d_s = ActivityTimeDogSitter.objects.create(
                activity_date=form.cleaned_data['activity_date'],
                activity_start=form.cleaned_data['activity_start'],
                activity_end=form.cleaned_data['activity_end'],
                username=username,
                user_id=user,
            )
            activity_d_s.save()
            messages.success(request, f'Activity time added successfully!')
            return redirect('activity_time')
    else:
        form = ActivityTimeDogSitterForm()

    return render(request, 'dogsitterService/add_activity_time.html', {'form': form})
