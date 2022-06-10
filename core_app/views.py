from random import random
#from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic.edit import DeleteView
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
#from datetime import datetime, timedelta
import json

from .forms import E2ETestParamsForm
from .models import E2ETestParams, E2ETestResults

TEST_RESULTS_TEMPLATE = 'core_app/pages/e2e-test-results-list.html'
ADD_TEST_TEMPLATE = 'core_app/pages/add-e2e-test.html'
EDIT_TEST_TEMPLATE = 'core_app/pages/edit-e2e-test.html'
DELETE_TEST_CONFIRM_TEMPLATE = 'core_app/pages/e2etestparams_confirm_delete.html'


class AddE2ETest(View):
    """Render scheduled tests and allow adding new tests.
    The class has two methods:
    GET - get all scheduled e2e-tests.
    POST - let the user add new e2e-tests.
    """

    def get(self, request, *args, **kwargs):
        # Show all scheduled e2e-tests
        all_scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        e2e_test_form = E2ETestParamsForm

        context = {
            'all_scheduled_tests': all_scheduled_tests,
            'e2e_test_form': e2e_test_form,
        }
        return render(request, ADD_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # Create an arbitrary schedule time for the e2e-test (for now)
        # schedule, _ = CrontabSchedule.objects.get_or_create(
        #                 minute='39',
        #                 hour='*',
        #                 day_of_week='*',
        #                 day_of_month='*',
        #                 month_of_year='*',
        #             )
        
        launches_per_day_raw = float(request.POST.get('launches_per_day'))
        # Round to not allow more than one test per minute
        launches_per_day_scaled_to_minutes = round(1440 / launches_per_day_raw)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=launches_per_day_scaled_to_minutes,
            period=IntervalSchedule.MINUTES,
        )

        # Schedule the e2e-test
        celery_task = PeriodicTask.objects.create(
            interval=schedule,                                 # created above.
            # crontab = schedule,
            name=str(request.user)+'_E2Etest_'+str(random()),   # describes this periodic task. Incremental
            task='core_app.tasks.call_crawl_website',           # name of task.
            args=json.dumps([request.POST.get('link')]),        # populate with variables from the POST form
            kwargs=json.dumps({}),
            #expires=datetime.utcnow() + timedelta(seconds=30)
            one_off=True
        )

        # POST to database
        e2e_test_form = E2ETestParamsForm(request.POST)

        if e2e_test_form.is_valid():
            # Connect between the Celery task and the app task
            new_test_job = e2e_test_form.save(commit=False)
            new_test_job.celery_task = celery_task
            new_test_job.save()

        # Reload the page with the newest data.
        # Show all scheduled tests
        all_scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        e2e_test_form = E2ETestParamsForm

        context = {
            'all_scheduled_tests': all_scheduled_tests,
            'e2e_test_form': e2e_test_form,
        }

        return render(request, ADD_TEST_TEMPLATE, context)


class EditE2ETest(View):
    """Render a scheduled test and allow to edit it.
    The class has two methods:
    GET - get a scheduled e2e-test.
    POST - let the user update parameters of the e2e-test.
    """

    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParams.objects.get(pk=pk)

        # instance=e2e_test_params will load the requested e2e-test form
        # with pre-filled fields.
        e2e_test_form = E2ETestParamsForm(instance=e2e_test_params) 

        context = {
            'e2e_test_params': e2e_test_params,
            'e2e_test_form': e2e_test_form,
        }
        return render(request, EDIT_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        """Update e2e-test settings.
        """
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParams.objects.get(pk=pk)

        # Update the e2e-test settings
        e2e_test_form = E2ETestParamsForm(request.POST, instance=e2e_test_params) 
        if e2e_test_form.is_valid():
            # TASK: Add a boolean to trigger a successful message as feedback
            e2e_test_form.save()

        context = {
            'e2e_test_params': e2e_test_params,
            'e2e_test_form': e2e_test_form,
            # TASK: Add a boolean to trigger a successful message as feedback
        }

        return render(request, EDIT_TEST_TEMPLATE, context)
    

class DeleteE2ETest(View):
    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test = E2ETestParams.objects.get(pk=pk)

        context = {
            'e2e_test': e2e_test,
        }
        return render(request, DELETE_TEST_CONFIRM_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test = E2ETestParams.objects.get(pk=pk)
        celery_task = PeriodicTask.objects.get(pk=e2e_test.celery_task.id)

        e2e_test.delete()
        celery_task.delete()

        # Go back to the page with all scheduled tests
        all_scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        e2e_test_form = E2ETestParamsForm

        context = {
            'all_scheduled_tests': all_scheduled_tests,
            'e2e_test_form': e2e_test_form,
        }
        return render(request, ADD_TEST_TEMPLATE, context)


class E2ETestResultsListView(generic.ListView):
    """List the results of scheduled e2e-tests.
    """
    model = E2ETestResults
    template_name = TEST_RESULTS_TEMPLATE
    paginate_by = 10