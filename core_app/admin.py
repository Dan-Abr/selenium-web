# Django
from django.contrib import admin

# local Django
from .models import E2ETestResults, E2ETestParams


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
        'created',
        'updated',
    ]

admin.site.register(E2ETestResults, E2ETestResultsAdmin)
admin.site.register(E2ETestParams, E2ETestParamsAdmin)