from django.db import models
from django_celery_beat.models import PeriodicTask


class E2ETestParams(models.Model):
    link = models.TextField()  # link --> url
    launches_per_day = models.FloatField()
    # ... list_of actions = [] ?

    celery_task = models.OneToOneField(PeriodicTask, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


# Create your models here.
class E2ETestResults(models.Model):
    link = models.TextField()  # link --> url
    page_title = models.CharField(max_length=200)
    status = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.link[:20]  # link --> url