# Django
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# local Django
from ..forms.forms_auth import *

LOGIN_TEMPLATE = 'core_app/auth/login.html'
REGISTER_TEMPLATE = 'core_app/auth/register.html'
SETTINGS_TEMPLATE = 'core_app/auth/user-settings.html'
CHANGE_PASSWORD_TEMPLATE = 'core_app/auth/change-password.html'



class UserRegisterView(SuccessMessageMixin, CreateView):
  template_name = REGISTER_TEMPLATE
  success_url = reverse_lazy('user-login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully. Please log in."



class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = CHANGE_PASSWORD_TEMPLATE
    success_url = reverse_lazy('user-change-password')
    form_class = UserPasswordChangeForm
    success_message = "Your profile was changed successfully."



class UserSettingsView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
  template_name = SETTINGS_TEMPLATE
  success_url = reverse_lazy('user-settings')
  form_class = UserSettingsForm
  success_message = "Your profile was changed successfully."

  def get_object(self):
    # Send the user's data to fill the form with the user's existing settings
    return self.request.user



class UserLoginView(View):
    def get(self, request, *args, **kwargs):
        user_login__form = UserLoginForm

        context = {
            'user_login__form': user_login__form,
        }
        return render(request, LOGIN_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        template_name = LOGIN_TEMPLATE
        form = UserLoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                if user.is_active:
                    # Login and redirect
                    login(request, user)
                    return redirect(reverse('create-e2e-test'))
                else:
                    messages.error(request, 'Account is disabled.')
                    return redirect(reverse('user-login'))
            else:
                messages.error(request, 'Username and/or password are invalid.')
                return redirect(reverse('user-login'))
        else:
            messages.error(request, 'Invalid attempt. Please try again.')
            return redirect(reverse('user-login'))



class UserLogoutView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        """Logout the user. Then, redirect to the login page.
        """
        logout(request)
        return redirect(reverse('user-login'))
