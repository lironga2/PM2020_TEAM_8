from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationFormDogOwner, RegistrationFormDogSitter
from account.models import Account as User
from gardens.models import ReportOnHazard
from home.models import GardenAdminNotice

from.forms import forms
# Create your views here.


def register_as_dog_owner(request):
    if request.method == 'POST':
        form = RegistrationFormDogOwner(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! you are now able to log in {username}!')
            return redirect('login')
    else:
        form = RegistrationFormDogOwner()
    return render(request, 'users/register_dog_owner.html', {'form': form})


def register_as_dog_sitter(request):
    if request.method == 'POST':
        form = RegistrationFormDogSitter(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = RegistrationFormDogSitter()
    return render(request, 'users/register_dog_sitter.html', {'form': form})


def d_o_profile(request):
    return render(request, 'users/d_o_profile.html')


def d_s_profile(request):
    return render(request, 'users/d_s_profile.html')


def d_g_a_profile(request):
    return render(request, 'users/d_g_a_profile.html')


def go_to_profile(request):
    if request.user.is_authenticated:
        u1 = User.objects.filter(username=request.user.username).first()
        test = ReportOnHazard.objects.all()
        admin_announcement = GardenAdminNotice.objects.all()
        #print(test)
        #return render(request, 'dogsitterService/view_service_requests.html', {"list": my_service_requests})
        if u1.is_dog_owner:
            #return redirect('d_o_profile',)
            return render(request, 'users/d_o_profile.html', {"list": admin_announcement})
        elif u1.is_dog_sitter:
            #return redirect('d_s_profile')
            return render(request, 'users/d_s_profile.html', {"list": admin_announcement})
        elif u1.is_dog_garden_admin:
            #return redirect('d_g_a_profile')
            return render(request, 'users/d_g_a_profile.html', {"list": admin_announcement})
        else:
            return redirect('site-home')
    else:
        return redirect('site-home')


def view_dog_sitters(request):
    users = User.objects.all()
    good = users.filter(is_dog_sitter=True)
    return render(request, 'users/view_dog_sitters.html', {"list": good})


