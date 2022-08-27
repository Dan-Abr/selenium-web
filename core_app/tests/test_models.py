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
    action_type_db_entry = None

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
                                                               e2e_test_params_pk=self.e2e_test_params_1.pk,
                                                               user=self.user_dummy_1
                                                               )

    def tearDown(self):
        User.objects.all().delete()
        PeriodicTask.objects.all().delete()
        E2ETestParamsModel.objects.all().delete()
        E2ETestResultsModel.objects.all().delete()


    # -----------------------------------------------------
    # Test models.
    # -----------------------------------------------------
    def test_E2ETestParamsModel_successfully_added_entry_to_db(self):
        # Verify the E2ETestParams was added to the database
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.url, 'https://google.com')

    def test_E2ETestParamsModel_has_user_field(self):
        # Verify the E2ETestParams was added to the database
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.user.username, 'test_user1')

    def test_E2ETestResultsModel_successfully_added_entry_to_db(self):
        # Verify the E2ETestResults added to the database
        e2e_test_results = E2ETestResultsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_results.url, 'https://google.com')

    def test_E2ETestResultsModel_is_not_deleted_when_its_E2ETestParamsModel_field_is_deleted(self):
        # Create end-to-end test
        e2e_test_results = E2ETestResultsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_results.url, 'https://google.com')
        # Delete e2e_test_params
        E2ETestParamsModel.objects.get(pk=1).delete()
        e2e_test_results = None
        # E2ETestResultsModel entry should not be deleted
        try:
            # Object should not be deleted
            e2e_test_results = E2ETestResultsModel.objects.get(pk=1)
        except:
            # Should be None
            e2e_test_results = None
        self.assertIsNotNone(e2e_test_results)
        # E2ETestResultsModel has access to the pk of a deleted E2ETestParamsModel
        self.assertEqual(e2e_test_results.e2e_test_params_pk, 1)

    def test_E2ETestParamsModel_entry_deleted_when_its_PeriodicTask_field_deleted(self):
        # Create end-to-end test
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.url, 'https://google.com')
        # Delete periodic_task
        PeriodicTask.objects.get(pk=1).delete()
        # E2ETestParamsModel entry should be deleted as well
        e2e_test_params = None
        try:
            # Object should be deleted
            e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        except:
            # Should be None
            e2e_test_params = None
        self.assertIsNone(e2e_test_params)

    def test_E2ETestParamsModel_entry_deleted_when_its_User_field_deleted(self):
        # Create end-to-end test
        e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        self.assertEqual(e2e_test_params.url, 'https://google.com')
        # Delete user
        User.objects.get(pk=1).delete()
        # E2ETestParamsModel entry should be deleted as well
        e2e_test_params = None
        try:
            # Object should be deleted
            e2e_test_params = E2ETestParamsModel.objects.get(pk=1)
        except:
            # Should be None
            e2e_test_params = None
        self.assertIsNone(e2e_test_params)

    def test_E2ETestActionModel_successfully_added_entry_db(self):
        # Verify E2ETestActionMode was added to the database
        action_type_db_entry = E2ETestActionModel.objects.create(event_type = 1,
                                                                 e2e_test_params = self.e2e_test_params_1)
        self.assertEqual(action_type_db_entry.event_type, 1)

    def test_E2ETestActionModel_can_access_its_E2ETestParamsModel_fields(self):
        # Verify E2ETestParamsModel is accessible from  E2ETestActionModel
        action_type_db_entry = E2ETestActionModel.objects.create(event_type = 1,
                                                                 e2e_test_params = self.e2e_test_params_1)
        self.assertEqual(action_type_db_entry.e2e_test_params.url, 'https://google.com')
        self.assertEqual(action_type_db_entry.e2e_test_params.user.username, 'test_user1')