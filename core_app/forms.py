from django import forms
from .models import *
#from django.contrib.auth.models import User


class E2ETestParamsForm(forms.ModelForm):
    class Meta:
        model = E2ETestParams
        fields = ['link', 'launches_per_day']

        # Style with Bootstrap
        widgets = {
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'launches_per_day': forms.NumberInput(attrs={'class': 'form-control'}), 
                }
                
        # Should not allow to edit fields:
        exclude = ['pk', 'celery_task']  


# class UserForm(forms.ModelForm):
#     # The user password field should be safe, type of 'PasswordInput'
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']