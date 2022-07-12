# Django
from django.contrib import admin

# local Django
from .models import E2ETestResultsModel, E2ETestParamsModel, E2ETestActionModel


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
        'user',
        'periodic_task',
        'start_date',
        'end_date',
        'enabled',
        'created',
        'updated',
    ]

class E2ETestActionAdmin(admin.ModelAdmin):
    list_display = [
        'e2e_test_params',
        'event_type',
        'wait_time_in_sec',
        'css_selector_click',
    ]

admin.site.register(E2ETestResultsModel, E2ETestResultsAdmin)
admin.site.register(E2ETestParamsModel, E2ETestParamsAdmin)
admin.site.register(E2ETestActionModel, E2ETestActionAdmin)