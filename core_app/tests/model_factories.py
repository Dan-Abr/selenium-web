# standard-library
from random import choice, randint
import string

# third-party
import factory
from faker import Faker
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# local Django
from ..models import *


fake = Faker()
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = fake.name()


class IntervalScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = IntervalSchedule
    
    every=10
    period=IntervalSchedule.MICROSECONDS


class PeriodicTaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PeriodicTask
    
    enabled = True
    interval = factory.SubFactory(IntervalScheduleFactory)
    # Random incremental string for the name
    name = factory.sequence(lambda n: ''.join([choice(string.ascii_lowercase)]))
    task = 'core_app.tasks.call_crawl_website'
    start_time = date.today().strftime('%Y-%m-%d')
    expires = None
    one_off=False


class E2ETestParamsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = E2ETestParamsModel

    url = "https://google.com"
    launches_per_day = randint(1,1440)
    start_date = date.today().strftime('%Y-%m-%d')
    enabled = True
    periodic_task = factory.SubFactory(PeriodicTaskFactory)
    user = factory.SubFactory(UserFactory)


class E2ETestActionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = E2ETestActionModel

    # Default to a wait event of 5 seconds.
    e2e_test_params = factory.SubFactory(E2ETestParamsModel)
    event_type = 1
    wait_time_in_sec = 5
    xpath_click = None


class E2ETestResultsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = E2ETestResultsModel

    # Default to a success result with no errors
    url = "https://google.com"
    page_title = "Google"
    status = "Success"
    error_list = []
    user = factory.SubFactory(UserFactory)
    e2e_test_params_pk = randint(0,100)