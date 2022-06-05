from django.contrib import admin
from .models import CrawlerResults


class CrawlerResultsAdmin(admin.ModelAdmin):
    list_display = [
        'link',
        'title',
        'status',
        'created',
        'updated'
    ]

admin.site.register(CrawlerResults, CrawlerResultsAdmin)