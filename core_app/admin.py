from django.contrib import admin
from .models import CrawlerResults, CrawlerParams


class CrawlerResultsAdmin(admin.ModelAdmin):
    list_display = [
        'link',
        'page_title',
        'status',
        'created',
        'updated'
    ]

class CrawlerParamsAdmin(admin.ModelAdmin):
    list_display = [
        'link',
    ]

admin.site.register(CrawlerResults, CrawlerResultsAdmin)
admin.site.register(CrawlerParams, CrawlerParamsAdmin)