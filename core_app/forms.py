# Django
from django import forms

# local Django
from .models import *


class E2ETestParamsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # Label with uppercase 
        super(E2ETestParamsForm, self).__init__(*args, **kwargs)
        self.fields['url'].label = "URL"

    class Meta:
        model = E2ETestParams
        fields = ['url', 'launches_per_day']

        # Style with Bootstrap
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
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