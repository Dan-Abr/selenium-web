# third-party
from ..models import *

# Django
from django.test import TestCase
from django.urls import reverse
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class TestModels(TestCase):
    periodic_task_1 = None
    e2e_test_params_1 = None
    e2e_test_results_1 = None

    def setUp(self):
        # Create a PeriodicTask in django celery beat. Will be used for scheduling e2e tests
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=50,
            period=IntervalSchedule.MINUTES,
        )

        periodic_task_1 = PeriodicTask.objects.create(
            interval=schedule,
            name='test_PeriodicTask',   
            task='core_app.tasks.call_crawl_website',           
        )

        self.e2e_test_params_1 = E2ETestParamsModel.objects.create(url='https://google.com', 
                                                               launches_per_day=1440, 
                                                               periodic_task=periodic_task_1
                                                               )
        self.e2e_test_results_1 = E2ETestResultsModel.objects.create(url='https://google.com', 
                                                               page_title='title', 
                                                               status='Passed'
                                                               )


    def tearDown(self):
        PeriodicTask.objects.all().delete()
        E2ETestParamsModel.objects.all().delete()
        E2ETestResultsModel.objects.all().delete()


    # ------------ Tests start here ------------
    def test_E2ETestParamsModel_successfully_added_new_e2e_test_to_db(self):
        # Verify the E2E test was added to the database
        user = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(user.url, 'https://google.com')

    def test_E2ETestResultsModel_successfully_added_result_test_to_db(self):
        # Verify the E2E test results added to the database
        user = E2ETestResultsModel.objects.get(pk=1)
        self.assertEqual(user.url, 'https://google.com')