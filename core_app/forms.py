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


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63)

    class Meta:
        model = User
        fields = ['username', 'password']


class E2ETestParamsForm(forms.ModelForm):
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
            # Allow end_date to be empty 
            'end_date': forms.DateInput(attrs={'class': 'form-control',  
                                                'name': 'date', 
                                                'type': 'text', 
                                                'placeholder': 'Leave empty if not applicable', 
                                                'onfocus': '(this.type="date")', 
                                                'onfocusout': '(this.type="text")'
                                                }), 
                }         
        # Should not allow to edit fields:
        exclude = ['pk', 'periodic_task']


class E2ETestActionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(E2ETestActionForm, self).__init__(*args, **kwargs)
        self.fields['xpath_click'].label = "XPath Click"

    class Meta:
        model = E2ETestActionModel
        fields = ['event_type', 'wait_time_in_sec', 'xpath_click',]
        # Style with Bootstrap
        widgets={
            'event_type': forms.Select(attrs={'class': 'form-control action-type',
                                              'required': 'required',}),
            'wait_time_in_sec': forms.NumberInput(attrs={
                                                        'class': 'form-control', 
                                                        'placeholder': ''
                                                        }),
            'xpath_click': forms.TextInput(attrs={'class': 'form-control', 
                                                        'placeholder': 'E.g. /html/body/div[1]/a[1]'
                                                        }),
        }


E2ETestActionFormsetCreate = modelformset_factory(
    model=E2ETestActionModel,
    form=E2ETestActionForm,
    extra=1,
    min_num=0, 
    validate_min=True,
    max_num=7,
    validate_max=True,
)


E2ETestActionFormsetEdit = modelformset_factory(
    model=E2ETestActionModel,
    form=E2ETestActionForm,
    extra=0,    # on edit, do not add new fields
    min_num=0, 
    validate_min=True,
    max_num=7,
    validate_max=True,
    can_delete=True,
    can_delete_extra=True,
)


class E2ETestActionFormsetCreateValidation(E2ETestActionFormsetCreate):
    # Since formsets are allowed to be empty, when using required fields
    # a manual validation must be performed.
    def __init__(self, *args, **kwargs):
        super(E2ETestActionFormsetCreateValidation, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
    def clear(self):
        if any(self.errors):
            return


class E2ETestActionFormsetEditValidation(E2ETestActionFormsetEdit):
    # Since formsets are allowed to be empty, when using required fields
    # a manual validation must be performed.
    def __init__(self, *args, **kwargs):
        super(E2ETestActionFormsetEditValidation, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
    
    def clear(self):
        if any(self.errors):
            return