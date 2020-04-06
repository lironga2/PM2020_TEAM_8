from django.shortcuts import render, redirect
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationFormDogOwner
from account.models import Account as User

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
