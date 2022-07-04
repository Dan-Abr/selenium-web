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


urlpatterns = [
    # Auth
    path('register/', UserRegisterPageView.as_view(), name='user-register'),
    path('login/', UserLoginPageView.as_view(), name='user-login'),
    path('logout/', 
         login_required(login_url='/login/')(UserLogoutPageView.as_view()), 
         name='user-logout'),

    # App
    path('',  
         login_required(login_url='/login/')(E2ETestResultsListView.as_view()), 
         name='e2e-test-results-list'),
    path('add-test/',  
         login_required(login_url='/login/')(AddE2ETest.as_view()), 
         name='add-e2e-test'),
    path('edit-test/<int:pk>',  
         login_required(login_url='/login/')(EditE2ETest.as_view()), 
         name='edit-e2e-test'),
    path('edit-test/<int:pk>/delete',  
         login_required(login_url='/login/')(DeleteE2ETest.as_view()), 
         name='delete-e2e-test'),
]
