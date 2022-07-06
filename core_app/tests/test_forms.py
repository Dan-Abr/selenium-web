# third-party
from ..forms import *

# Django
from django.test import TransactionTestCase
from django_celery_beat.models import PeriodicTask, IntervalSchedule


# Using TransactionTestCase instead of TestCase:
# https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
class TestE2ETestParamsModelForm(TransactionTestCase):
    form = None
    periodic_task = None
    user_dummy_credentials_1 = None
    user_dummy_1 = None

    def setUp(self):
        # Generate data for the form
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=50,
            period=IntervalSchedule.MINUTES,
        )

        self.periodic_task = PeriodicTask.objects.create(
            interval=schedule,
            name='test_PeriodicTask',   
            task='core_app.tasks.call_crawl_website',           
        )

        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }

        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        form_data = {'url': 'https://google.com', 'launches_per_day': 1, 'start_date':datetime.today()}
        self.form = E2ETestParamsModelForm(data=form_data)

    def tearDown(self):
        PeriodicTask.objects.all().delete()


    def test_addE2ETest_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.form.is_valid())

    def test_addE2ETest_valid_form_saved_fields(self):
        form_saved = None
        if self.form.is_valid():
            # Connect between the Django-beat database (celery) and the app's database
            form_saved = self.form.save(commit=False)
            form_saved.user = self.user_dummy_1
            form_saved.periodic_task = self.periodic_task
            form_saved.save()
        self.assertEqual(form_saved.url, 'https://google.com')


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