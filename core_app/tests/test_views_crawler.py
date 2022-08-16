# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404

# local Django
from .model_factories import *
from ..models import *
from ..forms import forms_crawler

class TestAuthViews(TestCase):
    login_url = None
    logout_url = None
    register_url_= None
    user_settings_url = None

    user_dummy_credentials_1 = None
    login_user_response = None
    user_dummy_1 = None

    create_e2e_test_url = None
    e2e_test_results_list_url = None
    
    def setUp(self):
        self.create_e2e_test_url = reverse('create-e2e-test')
        self.e2e_test_results_list_url = reverse('results-e2e-tests')

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
        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        # Login to the application
        self.login_user_response = self.client.post(self.login_url, self.user_dummy_credentials_1, follow=True)


    def tearDown(self):
        User.objects.all().delete()

    # -----------------------------------------------------
    # Test crawler views.
    # Below, I'm testing both factories and POST.
    # -----------------------------------------------------
    def test_user_created_successfully(self):
        # Can fetch page
        num = User.objects.all().count()
        self.assertEquals(num, 1)

    def test_GET_add_e2e_test_url(self):
        # Logged-in user can fetch inner pages
        response = self.client.get(self.create_e2e_test_url)
        self.assertEqual(response.status_code, 200)
    
    def test_GET_e2e_test_results_url(self):
        # Logged-in user can fetch inner pages
        response = self.client.get(self.e2e_test_results_list_url)
        self.assertEqual(response.status_code, 200)

    def test_GET_user_settings_url(self):
        # Logged-in user can fetch inner pages
        response = self.client.get(self.user_settings_url)
        self.assertEqual(response.status_code, 200)

    def test_FACTORY_e2e_test_with_valid_data_should_pass(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        result = get_object_or_404(E2ETestParamsModel, pk=1)
        self.assertEqual(result.url, 'https://bing.com')

    def test_FACTORY_edit_e2e_test_with_valid_data_should_pass(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        # Edit with new URL
        result = E2ETestParamsModel.objects.filter(pk=1).update(url='https://google.com')
        # Fetch again to make sure the value was updated
        result = get_object_or_404(E2ETestParamsModel, pk=1)
        self.assertEqual(result.url, 'https://google.com')

    def test_FACTORY_edit_e2e_test_with_invalid_data_should_fail(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        # Edit with invalid URL
        e2e_test_params_edit = forms_crawler.E2ETestParamsForm(instance=e2e_test_params).initial
        e2e_test_params_edit['url'] = 'https://'  # Invalid URL
        e2e_test_params_edit['end_date'] = ''
        post_response = self.client.post(
            reverse('edit-e2e-test', args=(e2e_test_params.id,)),
            e2e_test_params_edit,
            follow=True,
        )
        # URL still the same?
        self.assertContains(post_response, 'https://bing.com')

    def test_POST_edit_e2e_test_with_valid_data_should_pass(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        # Does the response contain the URL above?
        response = self.client.get(reverse('edit-e2e-test', args=(e2e_test_params.id,)), follow=True)
        self.assertContains(response, 'https://bing.com')
        # Edit e2e-test with a new URL
        e2e_test_params_edit = forms_crawler.E2ETestParamsForm(instance=e2e_test_params).initial
        e2e_test_params_edit['url'] = 'https://google.co.uk'
        e2e_test_params_edit['end_date'] = ''
        post_response = self.client.post(
            reverse('edit-e2e-test', args=(e2e_test_params.id,)),
            e2e_test_params_edit,
            follow=True,
        )
        # New URL updated?
        self.assertContains(post_response, 'https://google.co.uk')
        self.assertNotContains(post_response, 'https://bing.com')

    def test_POST_edit_e2e_test_with_invalid_data_should_fail(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        # Does the response contain the URL above?
        response = self.client.get(reverse('edit-e2e-test', args=(e2e_test_params.id,)), follow=True)
        self.assertContains(response, 'https://bing.com')
        # Edit e2e-test with an invalid URL field
        e2e_test_params_edit = forms_crawler.E2ETestParamsForm(instance=e2e_test_params).initial
        e2e_test_params_edit['url'] = 'invalid_url'
        e2e_test_params_edit['end_date'] = ''
        post_response = self.client.post(
            reverse('edit-e2e-test', args=(e2e_test_params.id,)),
            e2e_test_params_edit,
            follow=True,
        )
        # Does the URL still the same?
        self.assertContains(post_response, 'https://bing.com')
        self.assertNotContains(post_response, 'non_url')

    def test_POST_delete_e2e_test_should_pass(self):
        e2e_test_params = E2ETestParamsFactory.create(url='https://bing.com')
        # Does the deletion page shows a warning message of deletion?
        response = self.client.get(reverse('delete-e2e-test', args=(e2e_test_params.id,)), follow=True)
        self.assertContains(response, 'Are you sure you want to delete')
        # Redirect after deletion
        post_response = self.client.post(reverse('delete-e2e-test', args=(e2e_test_params.id,)), follow=True)
        self.assertRedirects(post_response, reverse('manage-e2e-tests'), status_code=302)

