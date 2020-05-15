from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from dogsitterService.forms import ActivityTimeDogSitterForm, UpdateMeetingActivity
from dogsitterService.models import ActivityTimeDogSitter, ServiceRequests, Meetings, MeetingsActivity
from dogsitterService.models import RejectedActivity, ServiceRejected, CanceledActivity, CanceledMeetings
from account.models import Account
from django.views.generic import ListView,DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


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
            my_meetings = MeetingsActivity.objects.filter(dogsitter_id=id)
            # need to create bool function for this check..
            for i in myactivities:
                if i.activity_date == form.cleaned_data['activity_date']:
                    if form.cleaned_data['activity_start'] > i.activity_start and form.cleaned_data[
                        'activity_start'] < i.activity_end or form.cleaned_data['activity_end'] > i.activity_start and \
                            form.cleaned_data['activity_end'] < i.activity_end:
                        messages.warning(request, f'Activity time is overlapped!')
                        return redirect('add_activity_time')
                    if form.cleaned_data['activity_start'] == i.activity_start or form.cleaned_data[
                        'activity_end'] == i.activity_end:
                        messages.warning(request, f'Activity time already exists!')
                        return redirect('add_activity_time')

            for i in my_meetings:
                if i.activity_date == form.cleaned_data['activity_date']:
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


def meeting_approval(request):
    service_id = request.GET['service_request']
    service_request = ServiceRequests.objects.filter(id=service_id).first()
    activity = service_request.activity_id
    print(activity)
    new_meeting_activity = MeetingsActivity.objects.create(
        activity_date=activity.activity_date,
        activity_start=activity.activity_start,
        activity_end=activity.activity_end,
        dogsitter_id=activity.user_id
    )
    new_meeting_activity.save()
    if new_meeting_activity:
        new_meeting = Meetings.objects.create(
            dog_owner_id=service_request.requesting_user,
            meetings_activity_id=new_meeting_activity
        )
        if new_meeting:
            service_request.delete()
            activity.delete()
            messages.success(request, f'The service request approved successfully! and new meeting has been created!')
        else:
            new_meeting_activity.delete()
            messages.warning(request, f'The service request isn׳t approved try again!')
    else:
        messages.warning(request, f'The service request isn׳t approved try again!')
    return redirect('view_service_requests')


def meeting_rejected(request):
    service_id = request.GET['service_request']
    service_request = ServiceRequests.objects.filter(id=service_id).first()
    activity = service_request.activity_id
    new_rejected_activity = RejectedActivity.objects.create(
        activity_date=activity.activity_date,
        activity_start=activity.activity_start,
        activity_end=activity.activity_end,
        dogsitter_id=activity.user_id
    )
    new_rejected_activity.save()
    if new_rejected_activity:
        new_service_rejected = ServiceRejected.objects.create(
            dog_owner_id=service_request.requesting_user,
            rejected_activity_id=new_rejected_activity
        )
        new_service_rejected.save()
        if new_service_rejected:
            service_request.delete()
            messages.success(request, f'The service request rejected successfully! and new meeting has been created!')
        else:
            new_rejected_activity.delete()
            messages.warning(request, f'The service request isn׳t rejected try again!')
    else:
        messages.warning(request, f'The service request isn׳t rejected try again!')
    return redirect('view_service_requests')


def view_my_meetings_dog_owner(request):
    my_meetings = Meetings.objects.filter(dog_owner_id=request.user)
    my_cancel_meetings = CanceledMeetings.objects.filter(dog_owner_id=request.user)
    my_rejected_requests = ServiceRejected.objects.filter(dog_owner_id=request.user)
    print(my_meetings)
    print(request.user)
    print(my_rejected_requests)
    #dogsitters = Account.objects.all()
    #return render(request, 'dogsitterService/dogsitter_service_coordination.html', context={'dogsitters': dogsitters, 'dogsitters_activity': dogsitters_activity})
    return render(request, 'dogsitterService/my_meetings_d_o.html', context={'my_meetings': my_meetings, 'my_rejected_requests': my_rejected_requests, 'my_cancel_meetings': my_cancel_meetings})


def cancel_meeting(request):
    meeting_id = request.GET['meeting_id']
    meeting = Meetings.objects.filter(id=meeting_id).first()
    activity = meeting.meetings_activity_id
    new_canceled_activity = CanceledActivity.objects.create(
        activity_date=activity.activity_date,
        activity_start=activity.activity_start,
        activity_end=activity.activity_end,
        dogsitter_id=activity.dogsitter_id
    )
    new_canceled_activity.save()
    if new_canceled_activity:
        new_canceled_meeting = CanceledMeetings.objects.create(
            dog_owner_id=meeting.dog_owner_id,
            rejected_activity_id=new_canceled_activity
        )
        new_canceled_activity.save()
        if new_canceled_activity:
            meeting.delete()
            activity.delete()
            messages.success(request, f'The meeting is canceled successfully!')
        else:
            new_canceled_activity.delete()
            messages.warning(request, f'The meeting isn׳t canceled try again!')
    else:
        messages.warning(request, f'The meeting isn׳t canceled try again!')
    if request.user.is_dog_sitter:
        return redirect('view_my_meetings_dogsitter')
    elif request.user.is_dog_owner:
        return redirect('view_my_meetings_dog_owner')
    else:
        return redirect('go_to_profile')


def view_my_meetings_dogsitter(request):
    all_meetings = Meetings.objects.all()
    my_meetings = []

    all_canceled_meetings = CanceledMeetings.objects.all()
    my_cancel_meetings = []

    all_rejected_requests = ServiceRejected.objects.all()
    my_rejected_requests = []

    for i in all_meetings:
        if i.meetings_activity_id.dogsitter_id == request.user:
            my_meetings.append(i)

    for i in all_canceled_meetings:
        if i.rejected_activity_id.dogsitter_id == request.user:
            my_cancel_meetings.append(i)

    for i in all_rejected_requests:
        if i.rejected_activity_id.dogsitter_id == request.user:
            my_rejected_requests.append(i)
    print(my_meetings)
    print(request.user)
    print(my_rejected_requests)
    #dogsitters = Account.objects.all()
    #return render(request, 'dogsitterService/dogsitter_service_coordination.html', context={'dogsitters': dogsitters, 'dogsitters_activity': dogsitters_activity})
    return render(request, 'dogsitterService/my_meetings_d_s.html', context={'my_meetings': my_meetings, 'my_rejected_requests': my_rejected_requests, 'my_cancel_meetings': my_cancel_meetings})


def update_meeting(request):

    activity_id = request.GET['meetings_activity_id']
    print('here!')
    print(activity_id)
    print('213123')
    meeting_activity = MeetingsActivity.objects.filter(id=activity_id).first()
    form = UpdateMeetingActivity(request.POST)
    if form.is_valid():
        id = request.user.id
        allactivities = ActivityTimeDogSitter.objects.all()
        myactivities = allactivities.filter(user_id=id)
        my_meetings = MeetingsActivity.objects.filter(dogsitter_id=id)
        #need to create bool function for this check..
        for i in myactivities:
            if form.cleaned_data['activity_start'] > form.cleaned_data['activity_end']:
                messages.warning(request, f'Activity start cant be later then activity end!')
                return redirect('view_my_meetings_dogsitter')
            if i.activity_date == form.cleaned_data['activity_date']:
                if i.id != meeting_activity.id and form.cleaned_data['activity_start'] > i.activity_start and \
                        form.cleaned_data[
                            'activity_start'] < i.activity_end or form.cleaned_data[
                    'activity_end'] > i.activity_start and \
                        form.cleaned_data['activity_end'] < i.activity_end and i.id != meeting_activity.id:
                    messages.warning(request, f'Activity time is overlapped!')
                    return redirect('view_my_meetings_dogsitter')
                if i.id != meeting_activity.id and form.cleaned_data['activity_start'] == i.activity_start or \
                        form.cleaned_data[
                            'activity_end'] == i.activity_end and i.id != meeting_activity.id:
                    messages.warning(request, f'Activity time already exists!')
                    return redirect('view_my_meetings_dogsitter')

        for i in my_meetings:
            if form.cleaned_data['activity_start'] > form.cleaned_data['activity_end']:
                messages.warning(request, f'Activity start cant be later then activity end!')
                return redirect('view_my_meetings_dogsitter')
            if i.activity_date == form.cleaned_data['activity_date']:
                if i.id != meeting_activity.id and form.cleaned_data['activity_start'] > i.activity_start and form.cleaned_data[
                    'activity_start'] < i.activity_end or form.cleaned_data['activity_end'] > i.activity_start and \
                        form.cleaned_data['activity_end'] < i.activity_end and i.id != meeting_activity.id:
                    messages.warning(request, f'Activity time is overlapped!')
                    return redirect('view_my_meetings_dogsitter')
                if i.id != meeting_activity.id and form.cleaned_data['activity_start'] == i.activity_start or form.cleaned_data[
                    'activity_end'] == i.activity_end and i.id != meeting_activity.id:
                    messages.warning(request, f'Activity time already exists!')
                    return redirect('view_my_meetings_dogsitter')

        #meeting_activity.activity_date = form.cleaned_data['activity_date']
        meeting_activity.activity_start = form.cleaned_data['activity_start']
        meeting_activity.activity_end = form.cleaned_data['activity_end']
        meeting_activity.save()
        messages.success(request, f'Activity time added successfully!')
        return redirect('view_my_meetings_dogsitter')
    else:
        form = UpdateMeetingActivity()

    return render(request, 'dogsitterService/update_meeting.html', {'form': form})


