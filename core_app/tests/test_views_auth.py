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

    home_page_url = None

    def setUp(self):
        self.home_pate_url = reverse('results-e2e-tests')

        self.login_url = reverse('user-login')
        self.logout_url = reverse('user-logout')
        self.register_url = reverse('user-register')
        self.user_settings_url = reverse('user-settings')
        self.user_change_password_url = reverse('user-change-password')

        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'email': 'test1@tests.com',
            'password': 'Test12321',
        }

        # Create Django's default user 
        User.objects.create_user(**self.user_dummy_credentials_1)

        # Login to the application
        self.login_user_response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)

    def tearDown(self):
        User.objects.all().delete()


    # -----------------------------------------------------
    # Test auth views
    # -----------------------------------------------------
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
        response = self.client.get(self.home_pate_url)
        self.assertEqual(response.status_code, 302)


    def test_GET_inner_page_redirect_if_not_logged_in(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # The response should redirect to the login page
        response = self.client.get(self.home_pate_url)
        self.assertEqual(response.status_code, 302)


    def test_GET_inner_page_is_visible_if_logged_in(self):
        response = self.client.get(self.home_pate_url)
        self.assertEqual(response.status_code, 200)


    def test_POST_register_no_data_no_redirect(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # Delete all users
        User.objects.all().delete()
        # Try to register with empty data
        response = self.client.post(self.register_url, data={})
        # Can't fetch inner pages
        response = self.client.get(self.home_pate_url)
        self.assertEqual(response.status_code, 302)


    def test_POST_register_valid_data_redirect(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # Delete all users
        User.objects.all().delete()
        # Try to register with valid data
        User.objects.create_user(**self.user_dummy_credentials_1)
        response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)
        # Can fetch inner pages
        response = self.client.get(self.home_pate_url)
        self.assertEqual(response.status_code, 200)


    def test_GET_edit_user_settings(self):
        response = self.client.get(self.user_settings_url)
        self.assertEqual(response.status_code, 200)

    
    def test_POST_change_user_settings_email(self):
        response = self.client.post(self.user_settings_url, {'email': 'test2@tests.com'}, follow=True)
        self.assertTrue(response.context['user'].email, 'test2@tests.com')


    def test_GET_user_change_password_settings_logged_out_redirect(self):
        # Logout
        response = self.client.get(self.logout_url, follow=True)
        # Delete all users
        User.objects.all().delete()
        response = self.client.get(self.user_change_password_url)
        self.assertEqual(response.status_code, 302)


    def test_GET_user_change_password_settings(self):
        response = self.client.get(self.user_change_password_url)
        self.assertEqual(response.status_code, 200)
