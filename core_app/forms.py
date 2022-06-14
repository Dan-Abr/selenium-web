# Django
from django import forms
# from django.contrib.admin.widgets import AdminDateWidget, AdminSplitDateTime

# local Django
from .models import *


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


# class UserForm(forms.ModelForm):
#     # The user password field should be safe, type of 'PasswordInput'
#     password = forms.CharField(widget=forms.PasswordInput())

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']