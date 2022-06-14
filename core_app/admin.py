# Django
from django.contrib import admin

# local Django
from .models import E2ETestResultsModel, E2ETestParamsModel


class E2ETestResultsAdmin(admin.ModelAdmin):
    list_display = [
        'url',
        'page_title',
        'status',
        'created',
        'updated',
    ]

class E2ETestParamsAdmin(admin.ModelAdmin):
    list_display = [
        'url',
        'launches_per_day',
        'enabled',
        'created',
        'updated',
    ]

admin.site.register(E2ETestResultsModel, E2ETestResultsAdmin)
admin.site.register(E2ETestParamsModel, E2ETestParamsAdmin)