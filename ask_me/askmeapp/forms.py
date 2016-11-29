# -*- coding: utf-8 -*-
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.files import File
from askmeapp.models import *
from django import forms


class LoginForm(forms.Form):
    login = forms.CharField(
        label='Login',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username here', }),
        max_length=30
    )
    password = forms.CharField(
        label='Password',
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
        label='Login',
        widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Enter your Username here', }),
        max_length=30
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'example@mail.ru', }),
        max_length=100
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
        min_length=8
    )
    password_repeat = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={ 'class': 'form-control', 'placeholder': '********' }),
        min_length=8
    )
    avatar = forms.FileField(
        label='Avatar',
        widget=forms.ClearableFileInput(),
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
        return pswd_repeat

    def clean_email(self):
        email = self.cleaned_data.get('email', '')

        try:
            e = User.objects.get(email=email)
            raise forms.ValidationError('Email is already used')
        except User.DoesNotExist:
            return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar is not None:
            if 'image' not in avatar.content_type:
                raise forms.ValidationError('Wrong image type')
        return avatar

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

class ChangePasswordForm(forms.Form):

    # def __init__(self, user):
    #     self._user = user

    password_old = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        min_length=8
    )
    password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        min_length=8
    )
    password_repeat = forms.CharField(
        label='Repeat Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
        min_length=8
    )




    def clean_password_old(self):
        oldpswd = self.cleaned_data.get('password_old')
        pswd = self.cleaned_data.get('password')
        print self._user.check_password(oldpswd)
        if oldpswd == pswd:
            raise forms.ValidationError('old and new password matched')
        if self._user.check_password(oldpswd):
            raise forms.ValidationError('Wrong old password')
        return oldpswd


    def clean_password_repeat(self):
        pswd = self.cleaned_data.get('password', '')
        pswd_repeat = self.cleaned_data.get('password_repeat', '')

        if pswd != pswd_repeat:
            raise forms.ValidationError('Passwords does not matched')
        return pswd_repeat

    def save(self, user):
        password = self.cleaned_data.get('password', '')
        if password is not None and password != '':
            #user.password = make_password(password)
            user.set_password(password)
            user.save()

        return self

class ProfileEditForm(forms.Form):

    information = forms.CharField(
        label='User Info',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4', 'placeholder': 'Enter information about yourself'}),
        required=False
    )

    avatar = forms.FileField(
        label='Avatar',
        widget=forms.ClearableFileInput(),
        required=False
    )



    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')

        if avatar is not None:
            if 'image' not in avatar.content_type:
                raise forms.ValidationError('Wrong image type')
        return avatar


    def save(self, user):
        data = self.cleaned_data

        up = user.profile
        up.information = data.get('information')

        if data.get('avatar') is not None:
            avatar = data.get('avatar')
            up.avatar.save('%s_%s' % (user.username, avatar.name), avatar, save=True)

        up.save()

        return self

class QuestionForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question title here', }),
        max_length=100
    )
    text = forms.CharField(
        label='Text',
        widget=forms.Textarea(attrs={'class': 'form-control noresize', 'rows': '14', 'placeholder': 'Enter your question here',}),
        max_length=100000
    )
    category = forms.CharField(
        label='Category',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter question categoty', }),
        max_length=50,
        required=False
    )
    tag1 = forms.CharField(
        label='Tags',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag 1'}),
        required=False
    )
    tag2 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag 2'}),
        required=False
    )
    tag3 = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag 3'}),
        required=False
    )

    def check_tag(self, tag):
        if (' ' in tag) or ('\n' in tag) or('\t' in tag) :
            raise forms.ValidationError('Tag contains spaces')
        if ('/' in tag) or ('\\' in tag) or ('?' in tag):
            raise forms.ValidationError('You can use only this symbols -+_~&@*%$')
        return tag

    def clean_tag1(self):
        tag = self.cleaned_data.get('tag1', '')
        return self.check_tag(tag)

    def clean_tag2(self):
        tag = self.cleaned_data.get('tag2')
        return self.check_tag(tag)

    def clean_tag3(self):
        tag = self.cleaned_data.get('tag3')
        return self.check_tag(tag)

    def save(self, user, id):
        data = self.cleaned_data
        if id <= 0:
            q = Question.objects.create(title=data.get('title'), text=data.get('text'),
                                    user=user, is_published=True)
        else:
            q = Question.objects.get(pk=id)
            q.title = data.get('title')
            q.text = data.get('text')
        q.tags.clear()

        q.save()

        for tag_num in ['tag1', 'tag2', 'tag3']:
            tag_text = data.get(tag_num, '')
            if tag_text is not None and tag_text != '':
                tag = Tag.objects.get_or_create(text=tag_text)

                q.tags.add(tag[0])

        category_text = data.get('category')
        if category_text is not None and category_text != '':
            category = Category.objects.get_or_create(title=category_text)
        else:
            category = Category.objects.get_or_create(title='General')
        q.category = category[0]
        q.save()
        return q



class AnswerForm(forms.Form):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'placeholder': 'Enter your answer here', })
    )

    def save(self, question, user):
        data = self.cleaned_data
        return question.answer_set.create(text=data.get('text'), user=user)
