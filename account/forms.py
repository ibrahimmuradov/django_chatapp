from django import forms
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
import re

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg border-light bg-light-subtle', 'placeholder': 'Enter email address'}
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg border-light bg-light-subtle', 'placeholder': 'Enter password'}
    ))

    error_messages = {
        'invalid_login': "Please enter a correct email address and password. Note that both fields are case-sensitive.",
        'inactive': "This account is inactive.",
    }


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    username = forms.CharField()
    first_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('username', 'email',)

    def clean_email(self):
        email = self.cleaned_data['email']
        filter_email = UserBase.objects.filter(email=email).exists()

        if filter_email:
            raise forms.ValidationError('Email address already exists')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        search_username = UserBase.objects.filter(username=username).exists()

        filter_re = r"^(?=.{3,20}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$"

        if search_username:
            raise forms.ValidationError('Username already exists')
        elif not re.search(filter_re, username):
            raise forms.ValidationError('You can only use letters, numbers and dot in the username')

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', None)

        if not first_name.replace(" ", "").isalpha():
            raise forms.ValidationError('You must use only letters in the first name')

        return first_name

    def clean_password2(self):
        clean_data = self.cleaned_data

        password = clean_data['password']
        password2 = clean_data['password2']

        if len(password) < 5:
            raise forms.ValidationError('Your password must be at least 5 characters')
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError('Your password must use at least 1 letter')
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control form-control-lg bg-light-subtle border-light',
             'placeholder': 'Enter email address',
             'maxlength': '150', 'minlength': '7'}
        )
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control form-control-lg bg-light-subtle border-light',
             'placeholder': 'Enter username',
             'maxlength': '50', 'minlength': '3'}
        )
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control form-control-lg bg-light-subtle border-light',
             'placeholder': 'Enter first name',
             'maxlength': '30', 'minlength': '3'}
        )
        self.fields['first_name'].required = False
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control form-control-lg bg-light-subtle border-light',
             'placeholder': 'Enter password',
             'maxlength': '50', 'minlength': '5'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control form-control-lg bg-light-subtle border-light',
             'placeholder': 'Enter password again',
             'maxlength': '50', 'minlength': '5'}
        )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg border-light bg-light-subtle',
               'placeholder': 'Enter email address'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']

        filter_email = UserBase.objects.filter(email=email)

        if not filter_email:
            raise forms.ValidationError('No user account found with the email address you entered')

        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh',
               'placeholder': 'Enter new password',
               'maxlength': '50', 'minlength': '5'}
    ))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh',
               'placeholder': 'Enter new password again',
               'maxlength': '50', 'minlength': '5'}
    ))
    