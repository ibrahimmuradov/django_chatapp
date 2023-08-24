from django import forms
from account.models import UserBase#, Friends
import pathlib
from .models import Friends
import re

class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=50, min_length=3, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh'}
    ))
    email = forms.EmailField(max_length=150, min_length=7, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh'}
    ))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh'}
    ))
    about = forms.CharField(max_length=300, widget=forms.Textarea(
        attrs={'class': 'form-control form-control-lg bg-light-subtle border-ligh', 'rows': '4'}
    ))

    class Meta:
        model = UserBase
        fields = ('username', 'email', 'first_name', 'about', 'profile_photo')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['username'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = False
        self.fields['about'].required = False
        self.fields['profile_photo'].widget.attrs.update(
            {'type': 'hidden',
             'class': 'form-control form-control-lg bg-light-subtle border-ligh',
             }
        )

    def clean_email(self):
        email = self.cleaned_data['email']
        filter_email = UserBase.objects.exclude(email=self.request.user.email).filter(email=email).exists()

        if filter_email:
            raise forms.ValidationError('Email address already exists')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        search_username = UserBase.objects.exclude(username=self.request.user.username).filter(username=username).exists()

        if search_username:
            raise forms.ValidationError('Username already exists')

        filter_re = r"^(?=.{3,20}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$"

        if not re.search(filter_re, username):
            raise forms.ValidationError('You can only use letters, numbers and periods in the username.')

        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', None)

        if first_name and not first_name.replace(" ", "").isalpha():
            raise forms.ValidationError('You must use only letters in the first name')

        return first_name

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo', None)

        if profile_photo:
            photo_path = pathlib.Path(str(profile_photo)).suffix
            if photo_path not in ['.jpg', '.jpeg', '.png']:
                raise forms.ValidationError('You can only upload images in jpg, jpeg or png formats.')

        return profile_photo
