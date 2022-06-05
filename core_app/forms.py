from django import forms
from .models import *
#from django.contrib.auth.models import User


class CrawlerParamsForm(forms.ModelForm):
    class Meta:
        model = CrawlerParams
        fields = ['link',]


# class UserForm(forms.ModelForm):
#     # The user password field should be safe, type of 'PasswordInput'
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']