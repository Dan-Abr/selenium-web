# Django
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# local Django
from .models import *


class UserRegisterForm(UserCreationForm):
    # email = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password"
        self.fields['password2'].label = "Verify Password"

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        # Style with Bootstrap
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            }


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)


class E2ETestParamsModelForm(forms.ModelForm):
    # start_date = forms.DateField(widget=AdminDateWidget())
    # start_time = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(E2ETestParamsModelForm, self).__init__(*args, **kwargs)
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