# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.files import File
from askmeapp.models import Profile
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username here', }),
            max_length=30
            )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '*******', }),
            min_length=8
            )

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login', ''), password=data.get('password', ''))

        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('User is not active')
        else:
            raise forms.ValidationError('Wrong login or password')


class SignupForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Enter your Username here', }),
            max_length=30
            )
    email = forms.EmailField(
            widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'example@mail.ru', }),
            required = False, max_length=100
            )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
            min_length=8
            )
    password_repeat = forms.CharField(
            widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
            min_length=8
            )
    avatar = forms.FileField(
            widget=forms.ClearableFileInput(attrs={ 'class': 'ask-signup-avatar-input', }),
            required=False
            )

    def clean_username(self):
        username = self.cleaned_data.get('username', '')

        try:
            u = User.objects.get(username=username)
            raise forms.ValidationError('Username is already used')
        except User.DoesNotExist:
            return username

    def clean_password_repeat(self):
        pswd = self.cleaned_data.get('password', '')
        pswd_repeat = self.cleaned_data.get('password_repeat', '')

        if pswd != pswd_repeat:
            raise forms.ValidationError('Passwords does not matched')

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            e = User.objects.get(email=email)
            raise forms.ValidationError('Email is already used')
        except User.DoesNotExist:
            return email

    def save(self):
        data = self.cleaned_data
        password = data.get('password')
        u = User()

        u.username = data.get('username')
        u.password = make_password(password)
        u.email = data.get('email')
        u.is_active = True
        u.is_superuser = False
        u.save()

        up = Profile()
        up.user = u
        up.rating = 0

        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            up.avatar.save('%s_%s' % (u.username, avatar.name), avatar, save=True)

        up.save()

        return authenticate(username=u.username, password=password)