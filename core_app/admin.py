from django.contrib import admin
from .models import CrawlerTask


class DOMElementAdmin(admin.ModelAdmin):
    list_display = [
        'source',
        'link',
        'title',
        'created',
        'updated'
    ]

admin.site.register(CrawlerTask, DOMElementAdmin)