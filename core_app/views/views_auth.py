# Django
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# local Django
from ..forms import *


REGISTER_TEMPLATE = 'core_app/auth/register.html'
LOGIN_TEMPLATE = 'core_app/auth/login.html'


class UserRegisterPageView(SuccessMessageMixin, CreateView):
  template_name = REGISTER_TEMPLATE
  success_url = reverse_lazy('user-login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"


class UserLoginPageView(View):
    def get(self, request, *args, **kwargs):
        user_login__form = AuthenticationForm

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
                    return redirect(reverse('add-e2e-test'))
                else:
                    return HttpResponse("Your account is disabled.")
            else:
                return HttpResponse('No such user')
        else:
            return HttpResponse('Invalid Form')


class UserLogoutPageView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        """Logout the user. Then, redirect to the login page.
        """
        logout(request)
        return redirect(reverse('user-login'))