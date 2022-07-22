# third-party
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Django
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import  get_object_or_404

# local Django
from ..models import *


class TestAuthViews(TestCase):
    login_url = None
    logout_url = None
    register_url_= None
    user_settings_url = None

    user_dummy_credentials_1 = None
    login_user_response = None
    user_dummy_1 = None

    create_e2e_test_url = None
    edit_e2e_test_url = None
    delete_e2e_test_url = None
    e2e_test_results_list_url = None
    
    def setUp(self):
        self.create_e2e_test_url = reverse('create-e2e-test')
        # self.edit_e2e_test_url = reverse('edit-e2e-test')
        # self.delete_e2e_test_url = reverse('delete-e2e-test')
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
    # Test crawler views
    # -----------------------------------------------------

    def test_GET_add_e2e_test_url(self):
        # Can fetch page
        response = self.client.get(self.create_e2e_test_url)
        self.assertEqual(response.status_code, 200)
        
    
    # def test_POST_e2e_test_valid_data_pass(self):
    #     schedule, created = IntervalSchedule.objects.get_or_create(
    #         every=50,
    #         period=IntervalSchedule.MINUTES,
    #     )
    #     periodic_task = PeriodicTask.objects.create(
    #         interval=schedule,
    #         name='test_PeriodicTask',   
    #         task='core_app.tasks.call_crawl_website',           
    #     )
    #     e2e_test__dummy = {
    #         'url': 'https://google.com',
    #         'launches_per_day': float(1),
    #         'start_date': '2025-01-01',
    #         'end_date': '2025-01-01',
    #         'enabled': True,
    #         'periodic_task': periodic_task,
    #         'user': self.user_dummy_1,
    #     }
    #     response = self.client.post(self.add_e2e_test_url, **e2e_test__dummy)
    #     result = get_object_or_404(E2ETestParamsModel, pk=1)
    #     self.assertEqual(result.url, 'https://google.com')
        

    # def test_POST_e2e_test_invalid_data_fail(self):
    #     e2e__test_dummy = {
    #         'username': 'test_user1',
    #         'email': 'test1@tests.com',
    #         'password': 'Test12321',
    #     }
    #     response = self.client.post(self.add_e2e_test_url, e2e__test_dummy, follow=True)
    #     self.assertEqual(response.status_code, 200)

