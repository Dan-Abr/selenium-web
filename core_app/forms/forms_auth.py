# Django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm

# local Django
from ..models import *



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}))
    
    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Verify Password"

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']
        # Style with Bootstrap
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            }


class UserSettingsForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']
        exclude = ['username', 'password1', 'password2']


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'type': 'password'}))
    
    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = "Old Password"
        self.fields['new_password1'].label = "New Password"
        self.fields['new_password2'].label = "Verify Password"

    class Meta:
        model = User
        fields = ['old_password', 'password1', 'password2']
        # Style with Bootstrap
        widgets = {
            'old_password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}),
            'new_password1': forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
            'new_password2': forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}),
            }


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63)

    class Meta:
        model = User
        fields = ['username', 'password']