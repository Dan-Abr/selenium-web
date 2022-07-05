# standard library
from random import random
import json

# Django
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.forms import DateField
from django.contrib.auth.mixins import LoginRequiredMixin

# local Django
from ..forms import *
from ..models import E2ETestParamsModel, E2ETestResultsModel


REGISTER_TEMPLATE = 'core_app/auth/register.html'
LOGIN_TEMPLATE = 'core_app/auth/login.html'

TEST_RESULTS_TEMPLATE = 'core_app/pages/e2e_test_results_list.html'
ADD_TEST_TEMPLATE = 'core_app/pages/add_e2e_test.html'
EDIT_TEST_TEMPLATE = 'core_app/pages/edit_e2e_test.html'
DELETE_TEST_CONFIRM_TEMPLATE = 'core_app/pages/e2e_test_confirm_delete.html'


class AddE2ETest(LoginRequiredMixin, View):
    """Render scheduled tests and allow adding new tests.
    The class has two methods:
    GET - get all scheduled e2e-tests.
    POST - let the user add new e2e-tests.
    """

    def get(self, request, *args, **kwargs):
        # Show all scheduled e2e-tests
        all_scheduled_tests = E2ETestParamsModel.objects.filter().order_by('-created')
        e2e_test_params__form = E2ETestParamsModelForm

        context = {
            'all_scheduled_tests': all_scheduled_tests,
            'e2e_test_params__form': e2e_test_params__form,
        }
        return render(request, ADD_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # Calculate form variables for the Celery task (& database storage)
        launches_per_day_raw = float(request.POST.get('launches_per_day'))
        # Prevent more than one test per minute
        launches_per_day_scaled_to_microseconds = 86400000000/max(round(launches_per_day_raw), 1)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=launches_per_day_scaled_to_microseconds,
            period=IntervalSchedule.MICROSECONDS,
        )

        # Create a database-entry object
        e2e_test_params__form = E2ETestParamsModelForm(request.POST)

        # POST the entry to database
        if e2e_test_params__form.is_valid():
            # Connect between the Celery task and the app task
            e2e_test_params = e2e_test_params__form.save(commit=False)
            # e2e_test_launches_in_minutes = (max(round(launches_per_day_scaled_to_microseconds), 1)/1000000)/60
            # new_e2e_test_job.launches_per_day = 1440/e2e_test_launches_in_minutes

            # Schedule the e2e-test using Celery
            periodic_task = PeriodicTask.objects.create(
                enabled = True if request.POST.get('enabled') == "on" else False,
                interval=schedule,                                  # created above.
                name=str(request.user)+'_E2Etest_'+str(random()),   # describes this periodic task. Incremental
                task='core_app.tasks.call_crawl_website',           # name of task.
                args=json.dumps([request.user.pk, request.POST.get('url')]),  # pass params for call_crawl_website()
                kwargs=json.dumps({}),
                start_time = request.POST.get('start_date'),
                expires = None if request.POST.get('end_date') == "" else request.POST.get('end_date'),
                #one_off=True
            )

            e2e_test_params.user = request.user
            e2e_test_params.launches_per_day = request.POST.get('launches_per_day')
            if type(request.POST.get('start_date')) is type(DateField):
                e2e_test_params.start_date = request.POST.get('start_date')
            if type(request.POST.get('end_date')) is type(DateField):
                e2e_test_params.end_date = request.POST.get('end_date')
            e2e_test_params.periodic_task = periodic_task
            e2e_test_params.save()

        # Reload the page with the newest data.
        # Show all scheduled tests
        all_scheduled_tests = E2ETestParamsModel.objects.filter().order_by('-created')
        e2e_test_params__form = E2ETestParamsModelForm

        context = {
            'all_scheduled_tests': all_scheduled_tests,
            'e2e_test_params__form': e2e_test_params__form,
        }
        # Redirect instead of render to avoid multiple submissions on page refresh
        return redirect(reverse('add-e2e-test'))


class EditE2ETest(LoginRequiredMixin, View):
    """Render a scheduled test and allow to edit it.
    The class has two methods:
    GET - get a scheduled e2e-test.
    POST - let the user update parameters of the e2e-test.
    """

    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test = E2ETestParamsModel.objects.get(pk=pk)

        # instance=e2e_test will load the requested e2e-test form
        # with pre-filled fields.
        e2e_test_params__form = E2ETestParamsModelForm(instance=e2e_test) 

        context = {
            'e2e_test': e2e_test,
            'e2e_test_params__form': e2e_test_params__form,
        }
        return render(request, EDIT_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        """Update e2e-test settings.
        """
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_pk = self.kwargs.get('pk')
        e2e_test = E2ETestParamsModel.objects.get(pk=e2e_test_pk)
        
        # Calculate form variables for the Celery task (& database storage)
        launches_per_day_raw = float(request.POST.get('launches_per_day'))
        # Round to prevent more than one test per minute
        launches_per_day_scaled_to_microseconds = 86400000000/max(round(launches_per_day_raw), 1)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=launches_per_day_scaled_to_microseconds,
            period=IntervalSchedule.MICROSECONDS,
        )

        # Create a database-entry object
        e2e_test_params__form = E2ETestParamsModelForm(request.POST, instance=e2e_test) 
        
        # POST the entry to database
        if e2e_test_params__form.is_valid():
            # TASK: Add a boolean to trigger a successful message as feedback
            e2e_test_params__form.launches_per_day = request.POST.get('launches_per_day')
            if type(request.POST.get('start_date')) is type(DateField):
                e2e_test_params__form.start_date = request.POST.get('start_date')
            if type(request.POST.get('end_date')) is type(DateField):
                e2e_test_params__form.end_date = request.POST.get('end_date')
            e2e_test_params__form.end_date = request.POST.get('end_date')
            e2e_test_params__form.save()

        # Get the according Celery task from beat's PeriodicTask table & update
        periodic_task = PeriodicTask.objects.get(pk=e2e_test.periodic_task.id)
        # Update values in the Celery task
        periodic_task.enabled = True if request.POST.get('enabled') == "on" else False
        periodic_task.interval = schedule
        periodic_task.expires =  None if request.POST.get('end_date') == "" else request.POST.get('end_date')
        periodic_task.args = json.dumps([request.POST.get('url')])
        periodic_task.save()

        context = {
            'e2e_test': e2e_test,
            'e2e_test_params__form': e2e_test_params__form,
            # TASK: Add a boolean to trigger a successful message as feedback
        }

        return render(request, EDIT_TEST_TEMPLATE, context)
    

class DeleteE2ETest(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_pk = self.kwargs.get('pk')
        e2e_test = E2ETestParamsModel.objects.get(pk=e2e_test_pk)

        context = {
            'e2e_test': e2e_test,
        }
        return render(request, DELETE_TEST_CONFIRM_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_pk = self.kwargs.get('pk')
        e2e_test = E2ETestParamsModel.objects.get(pk=e2e_test_pk)
        # Get the according Celery task from beat's PeriodicTask table
        periodic_task = PeriodicTask.objects.get(pk=e2e_test.periodic_task.id)
        # Delete both
        e2e_test.delete()
        periodic_task.delete()

        # Return to the tests' page
        return redirect(reverse('add-e2e-test'))


class E2ETestResultsListView(LoginRequiredMixin, generic.ListView):
    """List the results of scheduled e2e-tests.
    """
    model = E2ETestResultsModel
    template_name = TEST_RESULTS_TEMPLATE
    paginate_by = 10