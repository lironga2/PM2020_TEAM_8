from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from dogsitterService.forms import ActivityTimeDogSitterForm
from dogsitterService.models import ActivityTimeDogSitter, ServiceRequests
from account.models import Account


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
                if i.activity_date == form.cleaned_data['activity_date']:
                    print('helloooooo')
                    if form.cleaned_data['activity_start'] > i.activity_start and form.cleaned_data[
                        'activity_start'] < i.activity_end or form.cleaned_data['activity_end'] > i.activity_start and \
                            form.cleaned_data['activity_end'] < i.activity_end:
                        messages.warning(request, f'Activity time is overlapped!')
                        return redirect('add_activity_time')
                    if form.cleaned_data['activity_start'] == i.activity_start or form.cleaned_data[
                        'activity_end'] == i.activity_end:
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


def view_dogsitter_service_coordination(request):
    dogsitters_activity = ActivityTimeDogSitter.objects.all()
    dogsitters = Account.objects.all()
    return render(request, 'dogsitterService/dogsitter_service_coordination.html', context={'dogsitters': dogsitters, 'dogsitters_activity': dogsitters_activity})


def add_service_request(request):
    activity_id = request.GET['activity_id']
    activity = ActivityTimeDogSitter.objects.filter(id=activity_id).first()
    check = ServiceRequests.objects.filter(activity_id=activity_id).first()
    if check and check.activity_id.id == activity.id and check.requesting_user.id == request.user.id:
        messages.warning(request,
                         f'You already sent service ensure request for current activity please wait for dogsitter response!!')
    else:
        new_request = ServiceRequests.objects.create(
            activity_id=activity,
            requesting_user=request.user
        )
        new_request.save()
        if new_request:
            messages.success(request, f'The service ensure request sent successfully!')
        else:
            messages.warning(request, f'The service ensure request isn׳t sent try again!')
    #return render(request, 'dogsitterService/dogsitter_service_coordination.html')
    return redirect('view_dogsitter_service_coordination')


def cancel_service_request(request):
    activity_id = request.GET['activity_id']
    activity = ActivityTimeDogSitter.objects.filter(id=activity_id).first()
    check = ServiceRequests.objects.filter(activity_id=activity_id).first()
    if check and check.activity_id.id == activity.id and check.requesting_user.id == request.user.id:
        check.delete()
        messages.success(request, f'The service ensure request aborted successfully!')
    else:
            messages.warning(request, f'You cant abort ensure request that you never sent!')
    #return render(request, 'dogsitterService/dogsitter_service_coordination.html')
    return redirect('view_dogsitter_service_coordination')


def view_service_requests(request):
    my_activities = ActivityTimeDogSitter.objects.filter(user_id=request.user.id)
    service_requests = ServiceRequests.objects.all()
    my_service_requests = []
    for i in service_requests:
        if i.activity_id.user_id == request.user:
            my_service_requests.append(i)
    return render(request, 'dogsitterService/view_service_requests.html', {"list": my_service_requests})