# Django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import modelformset_factory

# local Django
from .models import *


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

# class UserChangePasswordForm(PasswordChangeForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

#     class Meta:
#         model = User
#         fields = ['email']
#         exclude = ['username', 'password1', 'password2']


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class E2ETestParamsForm(forms.ModelForm):
    # start_date = forms.DateField(widget=AdminDateWidget())
    # start_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(E2ETestParamsForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = "URL"
        
        # Do not allow edit 'start_date' once it was set
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['start_date'].widget.attrs['readonly'] = True

    class Meta:
        model = E2ETestParamsModel
        fields = ['url', 'launches_per_day', 'start_date', 'end_date', 'enabled']

        # Style with Bootstrap
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'launches_per_day': forms.NumberInput(attrs={'class': 'form-control'}), 
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
                }
                
        # Should not allow to edit fields:
        exclude = ['pk', 'periodic_task']


E2ETestActionFormset = modelformset_factory(
    E2ETestActionModel,
    fields=('event_type', 'wait_time_in_sec', 'css_selector_click',),
    extra=1,
    widgets={
        'event_type': forms.Select(attrs={'class': 'form-control',}),
        'wait_time_in_sec': forms.NumberInput(attrs={'class': 'form-control','placeholder': '-----'}),
        'css_selector_click': forms.TextInput(attrs={'class': 'form-control','placeholder': '-----'}),
    }
)