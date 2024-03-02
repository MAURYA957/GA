from django.contrib.auth.models import User
from django import forms
from django.db import models


# from .models import Profile


class UserRegistration(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='users/%Y/%M', blank=True)

    def __str__(self):
        return self.title


class AddItem(models.Model):
    Partname = models.CharField(max_length=200, unique=True)
    Partcode = models.CharField(max_length=100, unique=True)
    Version =  models.CharField(max_length=100, unique=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='users/%Y/%M', blank=True)
