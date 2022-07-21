# third-party
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Django
from django.test import TransactionTestCase

# local Django
from ..forms.forms_crawler import *


class TestE2ETestParamsForm(TransactionTestCase):
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
        self.form = E2ETestParamsForm(data=form_data)

    def tearDown(self):
        E2ETestParamsModel.objects.all().delete()
        PeriodicTask.objects.all().delete()
        User.objects.all().delete()
        

    def test_createE2ETest_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.form.is_valid())

    def test_createE2ETest_valid_form_saved_fields(self):
        form_saved = None
        if self.form.is_valid():
            # Connect between the Django-beat database (celery) and the app's database
            form_saved = self.form.save(commit=False)
            form_saved.user = self.user_dummy_1
            form_saved.periodic_task = self.periodic_task
            form_saved.save()
        self.assertEqual(form_saved.url, 'https://google.com')



# Using TransactionTestCase instead of TestCase:
# https://stackoverflow.com/questions/21458387/transactionmanagementerror-you-cant-execute-queries-until-the-end-of-the-atom
class TestE2ETestActionForm(TransactionTestCase):
    formset = None
    e2e_test_form = None
    e2e_test_form_saved = None
    periodic_task = None
    user_dummy_credentials_1 = None
    user_dummy_1 = None

    def setUp(self):
        # Generate data for the form
        self.user_dummy_credentials_1 = {
            'username': 'test_user1',
            'password': 'Test12321',
        }
        # Generate all the required data for creating a formset
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=50,
            period=IntervalSchedule.MINUTES,
        )

        self.periodic_task = PeriodicTask.objects.create(
            interval=schedule,
            name='test_PeriodicTask',   
            task='core_app.tasks.call_crawl_website',           
        )

        # Create a user
        self.user_dummy_1 = User.objects.create_user(**self.user_dummy_credentials_1)

        # Create e2e-test
        e2e_test_form_data = {'url': 'https://google.com', 'launches_per_day': 1, 'start_date':datetime.today()}
        self.e2e_test_form = E2ETestParamsForm(data=e2e_test_form_data)

        if self.e2e_test_form.is_valid():
            # Connect between the Django-beat database (celery) and the app's database
            self.e2e_test_form_saved = self.e2e_test_form.save(commit=False)
            self.e2e_test_form_saved.user = self.user_dummy_1
            self.e2e_test_form_saved.periodic_task = self.periodic_task
            self.e2e_test_form_saved.save()

        # Simulate formset
        formset_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-0-event_type': '1',
            }

        self.formset = E2ETestActionFormsetCreate(formset_data)


    def tearDown(self):
        E2ETestActionModel.objects.all().delete()
        PeriodicTask.objects.all().delete()
        User.objects.all().delete()


    def test_createE2ETest_valid_form_returns_valid_response(self):
        # print("---------------------------------")
        # print(self.form.errors)
        # print("---------------------------------")
        self.assertTrue(self.formset.is_valid())

    def test_addFormset_valid_form_saved_fields(self):
        for form in self.formset:
            if form.is_valid():
                form_saved = form.save(commit=False)
                form_saved.e2e_test_params = self.e2e_test_form_saved
                form_saved.save()
        self.assertEqual(form_saved.event_type, 1)