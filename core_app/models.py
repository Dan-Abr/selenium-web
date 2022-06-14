# third-party
from django_celery_beat.models import PeriodicTask
from datetime import date, datetime

# Django
from django.db import models


class E2ETestParamsModel(models.Model):
    url = models.URLField()
    launches_per_day = models.FloatField()
    
    start_date = models.DateField(default=datetime.today())
    end_date = models.DateField(blank=True, null=True)
    enabled = models.BooleanField(default=True)
    # ... list_of actions = [] ?
    
    periodic_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url[:20]
    


# Create your models here.
class E2ETestResultsModel(models.Model):
    url = models.TextField()
    page_title = models.CharField(max_length=200)
    status = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url[:20]