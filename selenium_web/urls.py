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
# third-party
from rest_framework.schemas import get_schema_view

# Django
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings


urlpatterns = [
    path('', include('core_app.urls')),
    path('admin/', admin.site.urls),
    
    # API schema (Open API)
    path('apischema/', get_schema_view(
        title='Selenium-web REST API',
        description='API for interacting with users records',
        version='1.0',
    ), name='openapi-schmea'),

    # API Documentation (swagger docs)
    path('swagger-docs/', TemplateView.as_view(
         template_name = 'core_app/swagger-docs.html',
         extra_context = {'schema_url': 'openapi-schmea'},
    ), name='swagger_docs'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
