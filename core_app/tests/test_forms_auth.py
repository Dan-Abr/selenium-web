# third-party
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Django
from django.test import TransactionTestCase

# local Django
from ..forms import *


class TestUserPasswordChangeForm(TransactionTestCase):
    form = None
    user_dummy_credentials_1 = None
    user_dummy_1 = None

    def setUp(self):
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }
        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        form_data = {'old_password': 'Test12321', 
                     'new_password1': 'Test123212',
                     'new_password2': 'Test123212'}
        self.form = PasswordChangeForm(self.user_dummy_1, data=form_data)

    def tearDown(self):
        User.objects.all().delete()


    def test_password_change_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.form.is_valid())

    def test_password_hashed_to_more_than_20_chars_after_changing(self):
        form_saved = None
        if self.form.is_valid():
            form_saved = self.form.save(commit=False)
            form_saved.save()
        self.assertGreater(len(form_saved.password), 20)


class TestUserRegisterForm(TransactionTestCase):
    form = None
    user_dummy_credentials_1 = None

    def setUp(self):
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'email': 'test@tests.com',
            'password1': 'Test12321',
            'password2': 'Test12321',
        }
        self.form = UserRegisterForm(data=self.user_dummy_credentials_1)

    def tearDown(self):
        User.objects.all().delete()


    def test_register_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.form.is_valid())

    def test_register_valid_form_saved_fields(self):
        form_saved = None
        if self.form.is_valid():
            form_saved = self.form.save(commit=False)
            form_saved.save()
        self.assertEqual(form_saved.username, 'test_user1')


class TestUserLoginForm(TransactionTestCase):
    form = None
    user_dummy_credentials_1 = None

    def setUp(self):
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }
        self.form = UserLoginForm(data=self.user_dummy_credentials_1)

    def tearDown(self):
        User.objects.all().delete()


    def test_login_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.form.is_valid())

    def test_login_valid_form_saved_fields(self):
        username = None
        if self.form.is_valid():
            username = self.form.cleaned_data['username']
        self.assertEqual(username, 'test_user1')