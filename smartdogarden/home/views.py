from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import GardenAdminNoticeForm
from .models import GardenAdminNotice
from account.models import Account


# Create your views here.

def home(request):
    return render(request, 'home/home.html')


def garden_admin_add_announcement(request):
    # if request.method == 'POST':
    form = GardenAdminNoticeForm(request.POST)
    if form.is_valid():
        username = request.user.username
        user = request.user
        announcement = GardenAdminNotice.objects.create(
            announcement_text=form.cleaned_data['announcement_text'],
            announces_id=user,
        )
        announcement.save()
        messages.success(request, f'Announcement has published successfully!')
        return redirect('go_to_profile')
    else:
        form = GardenAdminNoticeForm()
    return render(request, 'home/garden_admin_add_announcement.html', {'form': form})


def garden_admin_edit_announcement_board(request):
    reports = GardenAdminNotice.objects.all()
    return render(request, 'home/view_annoucement_for_edit.html', {"list": reports})


def garden_admin_delete_announcement(request):
    report_id = request.GET['announcement_id']
    the_report = GardenAdminNotice.objects.filter(id=report_id).first()
    the_report.delete()
    the_report = GardenAdminNotice.objects.filter(id=report_id).first()
    if the_report:
        messages.warning(request, f'The annoucement report isnt delete!')
    else:
        messages.success(request, f'The annoucement report deleted successfully!')
    return redirect('edit_announcement_board')


def admin_view_all_users(request):
    return render(request, 'home/admin_view_users.html')


def admin_view_dogsitter_users(request):
    dogsitters_users = Account.objects.filter(is_dog_sitter=1)
    return render(request, 'home/admin_view_dogsiiter_users.html', {"list": dogsitters_users})


def admin_view_dog_owner_users(request):
    dog_owner_users = Account.objects.filter(is_dog_owner=1)
    return render(request, 'home/admin_view_dog_owner_users.html', {"list": dog_owner_users})


def admin_delete_user(request):
    user_id = request.GET['user_id']
    user = Account.objects.filter(id=user_id).first()
    user.delete()
    user = Account.objects.filter(id=user_id).first()
    if user:
        messages.warning(request, f'The user isnt deleted!')
    else:
        messages.success(request, f'The user deleted successfully!')
    return redirect('view_users')
