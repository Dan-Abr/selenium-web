# third-party
from django_celery_beat.models import PeriodicTask
from datetime import date, datetime

# Django
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


# Crawler tasks
ACTION_TYPE = (
    (1, ("wait")),
    (2, ("click")),
)


class E2ETestParamsModel(models.Model):
    url = models.URLField()
    # At least one test per day & max of one test per minute
    launches_per_day = models.IntegerField(validators=[MinValueValidator(1),
                                                       MaxValueValidator(1440)])
    start_date = models.DateField(default=datetime.today())
    end_date = models.DateField(blank=True, null=True)
    enabled = models.BooleanField(default=True)
    
    periodic_task = models.OneToOneField(PeriodicTask, db_index=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.url[:20]


class E2ETestActionModel(models.Model):
    e2e_test_params = models.ForeignKey(E2ETestParamsModel, on_delete=models.CASCADE)
    # default=0 for an empty event, enforcing the user to choose 
    # an event type.
    event_type = models.IntegerField(choices=ACTION_TYPE, default=0, blank=True, null=True)   
    wait_time_in_sec = models.IntegerField(blank=True, null=True, max_length=3)
    xpath_click = models.CharField(blank=True, null=True, max_length=1024)

    created = models.DateTimeField(auto_now_add=True)


class E2ETestResultsModel(models.Model):
    url = models.TextField()
    page_title = models.CharField(max_length=200)
    status = models.CharField(max_length=10)
    error_list = models.CharField(blank=True, null=True, max_length=120)
    # e2e_test_params_pk not as foreign key since it might be deleted
    # and it should not affect the saved results.
    e2e_test_params_pk = models.IntegerField(max_length=12)

    user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.url[:20]