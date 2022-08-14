# third-party
from rest_framework.test import APITestCase

# Django
from django.urls import reverse

# local Django
from .model_factories import *
from ..serializers import *


class SerializersTest(APITestCase):
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


    def test_E2ETestParamsSerializer_has_correct_data(self):
        # Create a dummy e2e-test object
        e2e_test_params_dummy = E2ETestParamsFactory.create()
        # Serialize the e2e-test object
        e2e_test_params_serializer = E2ETestParamsSerializer(instance=e2e_test_params_dummy)
        # Check if the serialized e2e-test object is equal to the original e2e-test parameters object
        self.assertEqual(e2e_test_params_serializer.data, E2ETestParamsSerializer(e2e_test_params_dummy).data)

    def test_E2ETestResultsSerializer_has_correct_data(self):
        # Create a dummy e2e-test object
        e2e_test_results_dummy = E2ETestResultsFactory.create()
        # Serialize the e2e-test object
        e2e_test_results_serializer = E2ETestResultsSerializer(instance=e2e_test_results_dummy)
        # Check if the serialized e2e-test object is equal to the original e2e-test parameters object
        self.assertEqual(e2e_test_results_serializer.data, E2ETestResultsSerializer(e2e_test_results_dummy).data)