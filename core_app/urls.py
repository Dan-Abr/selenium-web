"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""

from django.urls import include, path
from .views import *

urlpatterns = [
    path("", E2ETestResultsListView.as_view(), name="e2e-test-results-list"),
    path("add-test/", AddE2ETest.as_view(), name="add-e2e-test"),
    path("edit-test/<int:pk>", EditE2ETest.as_view(), name="edit-e2e-test"),
    path("edit-test/<int:pk>/delete", DeleteE2ETest.as_view(), name="delete-e2e-test"),
]
