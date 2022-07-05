# third-party
from ..models import *

# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestAuthViews(TestCase):
    login_url = None
    logout_url = None
    register_url_= None
    user_settings_url = None

    user_dummy_credentials_1 = None
    login_user_response = None

    e2e_test_results_list_url = None
    add_e2e_test_url = None
    edit_e2e_test_url = None
    delete_e2e_test_url = None

    def setUp(self):
        # self.e2e_test_results_list_url = reverse('e2e-test-results-list')
        self.add_e2e_test_url = reverse('add-e2e-test')
        # self.edit_e2e_test_url = reverse('edit-e2e-test')
        # self.delete_e2e_test_url = reverse('delete-e2e-test')

        self.login_url = reverse('user-login')
        self.logout_url = reverse('user-logout')
        self.register_url = reverse('user-register')
        # self.user-settings = reverse('user-settings')

        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }

        # Create Django's default user 
        User.objects.create_user(**self.user_dummy_credentials_1)

        # Login to the application
        self.login_user_response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)


    def tearDown(self):
        User.objects.all().delete()
        # UserProfile.objects.all().delete()

    # ------------ Tests start here ------------
    def test_GET_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)


    def test_GET_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)


    def test_user_is_logged_in_successfully(self):
        # Check if the user is active
        self.assertTrue(self.login_user_response.context['user'].is_active)


    def test_logged_out_user_cannot_fetch_inner_pages(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # Try fetching an inner page should redirect
        response = self.client.get(self.add_e2e_test_url)
        self.assertEqual(response.status_code, 302)


    def test_GET_inner_page_redirect_if_not_logged_in(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # The response should redirect to the login page
        response = self.client.get(self.add_e2e_test_url)
        self.assertEqual(response.status_code, 302)


    def test_GET_inner_page_is_visible_if_logged_in(self):
        # Get the timeline URL
        response = self.client.get(self.add_e2e_test_url)
        self.assertEqual(response.status_code, 200)


    def test_POST_register_no_data_no_redirect(self):
        # First, ensure is logout
        response = self.client.get(self.logout_url, follow=True)
        # Delete all users
        User.objects.all().delete()
        # Try to register with empty data
        response = self.client.post(self.register_url, data={})
        # Can't fetch inner pages
        response = self.client.get(self.add_e2e_test_url)
        self.assertEqual(response.status_code, 302)


    def test_POST_register_valid_data_redirect(self):
        # First, ensure is logout
        response = self.client.get(self.logout_url, follow=True)
        # Delete all users
        User.objects.all().delete()
        # Try to register with valid data
        User.objects.create_user(**self.user_dummy_credentials_1)
        response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)
        # Can fetch inner pages
        response = self.client.get(self.add_e2e_test_url)
        self.assertEqual(response.status_code, 200)