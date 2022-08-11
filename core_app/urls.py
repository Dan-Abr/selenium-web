"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django
from django.urls import include, path
from django.contrib.auth.decorators import login_required

# local Django
from .views.views_crawler import *
from .views.views_auth import *
from . import api


urlpatterns = [
    # Auth
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', 
         login_required(login_url='/login/')(UserLogoutView.as_view()), 
         name='user-logout'),
    path('user-settings/', 
         login_required(login_url='/login/')(UserSettingsView.as_view()), 
         name='user-settings'),
    path('password/', 
         login_required(login_url='/login/')(UserPasswordChangeView.as_view()), 
         name='user-change-password'),

    # App
    path('',  
         login_required(login_url='/login/')(E2ETestResultsListView.as_view()), 
         name='results-e2e-tests'),
    path('create-test/',  
         login_required(login_url='/login/')(CreateE2ETestView.as_view()), 
         name='create-e2e-test'),
     path('manage-tests/',  
         login_required(login_url='/login/')(ManageE2ETestsView.as_view()), 
         name='manage-e2e-tests'),
    path('edit-test/<int:pk>',  
         login_required(login_url='/login/')(EditE2ETestView.as_view()), 
         name='edit-e2e-test'),
    path('edit-test/<int:pk>/delete',  
         login_required(login_url='/login/')(DeleteE2ETestView.as_view()), 
         name='delete-e2e-test'),

     # API
     path('api/e2e-tests', api.E2ETestParamsList.as_view(), name='api-e2e-tests-list'),
     path('api/e2e-test-results', api.E2ETestResultsList.as_view(), name='api-e2e-test-results-list'),
]
