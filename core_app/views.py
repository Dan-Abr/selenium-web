from random import random
from django.shortcuts import redirect, render
from django.views import View, generic
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from datetime import datetime, timedelta
import json

from pyparsing import one_of, oneOf

from .forms import E2ETestParamsForm
from .models import E2ETestParams, E2ETestResults

TEST_RESULTS_TEMPLATE = 'pages/e2e-test-results-list.html'
ADD_TEST_TEMPLATE = 'pages/add-e2e-test.html'
EDIT_TEST_TEMPLATE = 'pages/edit-e2e-test.html'


class E2ETestResultsListView(generic.ListView):
    """_summary_

    Args:
        View (_type_): _description_
    """
    model = E2ETestResults
    template_name = TEST_RESULTS_TEMPLATE
    paginate_by = 10


class AddE2ETest(View):
    """Render scheduled tests and allow adding new tests.
    The class has two methods:
    GET - get all scheduled e2e-tests.
    POST - let the user add new e2e-tests.
    """

    def get(self, request, *args, **kwargs):
        # Show all scheduled tests
        scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        add_test_form = E2ETestParamsForm

        context = {
            'scheduled_tests': scheduled_tests,
            'add_test_form': add_test_form,
        }
        return render(request, ADD_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        add_test_form = E2ETestParamsForm(request.POST)

        # POST to database
        if add_test_form.is_valid():
            new_test_job = add_test_form.save(commit=False)
            new_test_job.save()

        # Reload the page with the newest data.
        # Show all scheduled tests
        scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        add_test_form = E2ETestParamsForm

        # Schedule the E2Etest automatically for now
        schedule, _ = CrontabSchedule.objects.get_or_create(
                        minute='39',
                        hour='*',
                        day_of_week='*',
                        day_of_month='*',
                        month_of_year='*',
                    )

        PeriodicTask.objects.create(
            #interval=schedule,                                 # created above.
            crontab = schedule,
            name=str(request.user)+'_E2Etest_'+str(random()),   # describes this periodic task. Incremental
            task='core_app.tasks.call_crawl_website',           # name of task.
            args=json.dumps([request.POST.get('link')]),        # populate with variables from the POST form
            kwargs=json.dumps({}),
            #expires=datetime.utcnow() + timedelta(seconds=30)
            one_off=True
        )

        context = {
            'scheduled_tests': scheduled_tests,
            'add_test_form': add_test_form,
        }

        return render(request, ADD_TEST_TEMPLATE, context)


class EditE2ETest(View):
    """Render a scheduled test and allow to edit it.
    The class has two methods:
    GET - get a scheduled e2e-test.
    POST - let the user update the e2e-test.
    """

    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParams.objects.get(pk=pk)

        # instance=profile will load the requested e2e-test form
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
            # TASK: Add a boolean to trigger a successful message
            e2e_test_form.save()

        context = {
            'e2e_test_params': e2e_test_params,
            'e2e_test_form': e2e_test_form,
            # TASK: Add a boolean to trigger a successful message
        }

        return render(request, EDIT_TEST_TEMPLATE, context)