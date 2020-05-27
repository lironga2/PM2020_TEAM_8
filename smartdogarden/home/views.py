from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .forms import GardenAdminNoticeForm
from .models import GardenAdminNotice

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
