# third-party
from ..models import *

# Django
from django.test import TestCase
from django.urls import reverse
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib.auth.models import User


class TestModels(TestCase):
    periodic_task_1 = None
    e2e_test_params_1 = None
    e2e_test_results_1 = None
    user_dummy_credentials_1 = None
    user_dummy_1 = None

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

        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }

        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        self.e2e_test_params_1 = E2ETestParamsModel.objects.create(url='https://google.com', 
                                                               launches_per_day=1440, 
                                                               periodic_task=periodic_task_1,
                                                               user=self.user_dummy_1,
                                                               )
        self.e2e_test_results_1 = E2ETestResultsModel.objects.create(url='https://google.com', 
                                                               page_title='title', 
                                                               status='Passed',
                                                               e2e_test_params=self.e2e_test_params_1,
                                                               user=self.user_dummy_1
                                                               )


    def tearDown(self):
        User.objects.all().delete()
        PeriodicTask.objects.all().delete()
        E2ETestParamsModel.objects.all().delete()
        E2ETestResultsModel.objects.all().delete()


    # ------------ Tests start here ------------
    def test_E2ETestParamsModel_successfully_added_new_e2e_test_to_db(self):
        # Verify the E2E test was added to the database
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.url, 'https://google.com')


    def test_E2ETestParamsModel_has_user_field(self):
        # Verify the E2E test was added to the database
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.user.username, 'test_user1')


    def test_E2ETestResultsModel_successfully_added_result_test_to_db(self):
        # Verify the E2E test results added to the database
        e2e_test_results = E2ETestResultsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_results.url, 'https://google.com')