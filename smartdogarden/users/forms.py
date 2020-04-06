from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from account.models import Account


class RegistrationFormDogOwner(UserCreationForm):
    email = forms.EmailField()
    user_id = Account.user_id

    class Meta:
        model = Account
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'user_id',
            'city',
            'street',
            'app_number',
            'zip',
            'phone_number',
        ]

    def save(self, commit=True):
        user = super(RegistrationFormDogOwner, self).save(commit=False)
        user.is_dog_owner = True
        if commit:
            user.save()

            return user


class RegistrationFormDogSitter(UserCreationForm):
    email = forms.EmailField()
    user_id = Account.user_id

    class Meta:
        model = Account
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'user_id',
            'phone_number',
        ]

    def save(self, commit=True):
        user = super(RegistrationFormDogSitter, self).save(commit=False)
        user.is_dog_sitter = True
        if commit:
            user.save()

            return user
