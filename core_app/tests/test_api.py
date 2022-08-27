# standard library
import json

# third-party
from rest_framework.test import APITestCase
from django_celery_beat.models import PeriodicTask

# Django
from django.urls import reverse

# local Django
from .model_factories import *
from ..serializers import *
from .model_factories import *


class APITest(APITestCase):
    user_dummy_credentials_1 = None
    login_url = None

    def setUp(self):
        self.login_url = reverse('user-login')

        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'email': 'test1@tests.com',
            'password': 'Test12321',
        }
        # Create Django's default user 
        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        # Login to the application
        self.login_user_response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)

    def tearDown(self):
        User.objects.all().delete()

    
    def test_E2ETestParamsList_returns_success(self):
        # Can access the user's e2e-tests via API endpoint?
        url = reverse('api-e2e-tests-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_E2ETestParamsList_returns_empty_list(self):
        # Since there are no e2e-tests, the list should be empty.
        url = reverse('api-e2e-tests-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_E2ETestParamsList_returns_list_of_e2e_tests(self):
        # Create a dummy e2e-tests.
        E2ETestParamsFactory.create(user=self.user_dummy_1)
        E2ETestParamsFactory.create(user=self.user_dummy_1)
        # API endpoint has two e2e-test.
        url = reverse('api-e2e-tests-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 1)
    
    def test_E2ETestParamsID_returns_success(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Can access the user's e2e-test via API endpoint?
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_E2ETestParamsID_returns_not_found(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Access non-existing e2e-test via API endpoint.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk + 1})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 404)

    def test_E2ETestParamsID_returns_e2e_test(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Verify e2e-test's parameters are returned.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        date_now = date.today().strftime('%Y-%m-%d')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], e2e_test_params.url)
        self.assertEqual(response.data['launches_per_day'], e2e_test_params.launches_per_day)
        self.assertEqual(response.data['user'], e2e_test_params.user.pk)
        self.assertEqual(response.data['start_date'], date_now)

    def test_E2ETestParamsID_delete_e2e_test(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Delete e2e-test via API endpoint.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        response = self.client.delete(url)
        response.render()
        self.assertEqual(response.status_code, 204)
        # Verify e2e-test has been deleted.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 404)

    def test_E2ETestParamsID_delete_e2e_test_deletes_PeriodicTask(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        periodic_task = e2e_test_params.periodic_task
        # Create a dummy e2e-test result.
        e2e_test_result = E2ETestResultsFactory.create(user=self.user_dummy_1)
        # Delete e2e-test result via API endpoint.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        response = self.client.delete(url)
        response.render()
        self.assertEqual(response.status_code, 204)
        # Verify e2e-test result has been deleted.
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 404)
        # Verify its PeriodicTask has been deleted (cascading).
        try:
            # Object should be deleted
            periodic_task = PeriodicTask.objects.get(pk=periodic_task.pk)
        except:
            # Should be None
            periodic_task = None
        self.assertIsNone(periodic_task)

    def test_E2ETestParamsID_edit_e2e_test(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Edit e2e-test's parameters.
        url = reverse('api-e2e-test-id', kwargs={'pk': e2e_test_params.pk})
        data = {
            'id': e2e_test_params.pk,
            'url': e2e_test_params.url,
            'launches_per_day': 200,  # Change from the random value to 200.
            'start_date': e2e_test_params.start_date,
            'end_date': "",
            'enabled': e2e_test_params.enabled,
            'created': e2e_test_params.created,
            'updated': e2e_test_params.updated,
            'periodic_task': e2e_test_params.periodic_task.pk,
            'user': e2e_test_params.user.pk,
        }
        response = self.client.put(url, data)
        e2e_test_params.refresh_from_db()
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], data['url'])
        self.assertEqual(response.data['launches_per_day'], data['launches_per_day'])
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['start_date'], data['start_date'])

    def test_E2ETestResultsList_returns_success(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Can access the user's e2e-test results via API endpoint?
        url = reverse('api-e2e-test-results-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)

    def test_E2ETestResultsList_returns_empty_list(self):
        # Since there are no e2e-test results, the list should be empty.
        url = reverse('api-e2e-test-results-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
    
    def test_E2ETestResults_returns_list_of_e2e_test_results(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Create a dummy e2e-test result.
        E2ETestResultsFactory.create(user=self.user_dummy_1)
        E2ETestResultsFactory.create(user=self.user_dummy_1)
        # API endpoint has two e2e-test result.
        url = reverse('api-e2e-test-results-list')
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 1)

    def test_E2ETestResultsID_returns_e2e_test_result(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Create a dummy e2e-test result.
        e2e_test_result = E2ETestResultsFactory.create(user=self.user_dummy_1)
        # Verify e2e-test result's parameters are returned.
        url = reverse('api-e2e-test-result-id', kwargs={'pk': e2e_test_result.pk})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], e2e_test_result.url)
        self.assertEqual(response.data['user'], e2e_test_result.user.pk)
        self.assertEqual(response.data['e2e_test_params_pk'], e2e_test_result.e2e_test_params_pk)
        self.assertEqual(response.data['page_title'], e2e_test_result.page_title)
        self.assertEqual(response.data['status'], e2e_test_result.status)

    def test_E2ETestResultsID_delete_e2e_test_result(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Create a dummy e2e-test result.
        e2e_test_result = E2ETestResultsFactory.create(user=self.user_dummy_1)
        # Delete e2e-test result via API endpoint.
        url = reverse('api-e2e-test-result-id', kwargs={'pk': e2e_test_result.pk})
        response = self.client.delete(url)
        response.render()
        self.assertEqual(response.status_code, 204)
        # Verify e2e-test result is deleted.
        url = reverse('api-e2e-test-result-id', kwargs={'pk': e2e_test_result.pk})
        response = self.client.get(url)
        response.render()
        self.assertEqual(response.status_code, 404)

    def test_E2ETestResultID_edit_e2e_test_result(self):
        # Create a dummy e2e-tests.
        e2e_test_params = E2ETestParamsFactory.create(user=self.user_dummy_1)
        # Create a dummy e2e-test result.
        e2e_test_result = E2ETestResultsFactory.create(user=self.user_dummy_1)
        # Edit e2e-test result's parameters.
        url = reverse('api-e2e-test-result-id', kwargs={'pk': e2e_test_result.pk})
        data = {
            'id': e2e_test_result.pk,
            'url': "https://www.bing.com",  # Change Google to Bing
            'user': e2e_test_result.user.pk,
            'page_title': e2e_test_result.page_title,
            'e2e_test_params_pk': e2e_test_params.pk,
            'status': e2e_test_result.status,
            'created': e2e_test_result.created,
            'updated': e2e_test_result.updated,
        }
        response = self.client.put(url, 
                                   json.dumps(data, sort_keys=True, default=str), 
                                   content_type='application/json'
                                   )
        e2e_test_result.refresh_from_db()
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['url'], data['url'])
        self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['page_title'], data['page_title'])
        self.assertEqual(response.data['status'], data['status'])