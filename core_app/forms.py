from django import forms
from .models import *
#from django.contrib.auth.models import User


class E2ETestParamsForm(forms.ModelForm):
    class Meta:
        model = E2ETestParams
        fields = ['link',]

        # Style with Bootstrap
        widgets = {
            'link': forms.TextInput(attrs={'class': 'form-control'}),
        }


# class UserForm(forms.ModelForm):
#     # The user password field should be safe, type of 'PasswordInput'
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']