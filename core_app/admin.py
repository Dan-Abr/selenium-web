from django.contrib import admin
from .models import TestResults, TestParams


class TestResultsAdmin(admin.ModelAdmin):
    list_display = [
        'link',
        'page_title',
        'status',
        'created',
        'updated',
    ]

class TestParamsAdmin(admin.ModelAdmin):
    list_display = [
        'link',
        'created',
        'updated',
    ]

admin.site.register(TestResults, TestResultsAdmin)
admin.site.register(TestParams, TestParamsAdmin)