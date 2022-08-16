# standard library
from random import random
import json

# third-party
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# Django
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View, generic
from django.forms import DateField
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# local Django
from ..forms.forms_crawler import *
from ..utils import e2e_test_action_form_to_dict
from ..models import E2ETestParamsModel, E2ETestResultsModel, E2ETestActionModel


REGISTER_TEMPLATE = 'core_app/auth/register.html'
LOGIN_TEMPLATE = 'core_app/auth/login.html'

TEST_RESULTS_TEMPLATE = 'core_app/e2e-tests/results.html'
CREATE_TEST_TEMPLATE = 'core_app/e2e-tests/create.html'
MANAGE_TESTS_TEMPLATE = 'core_app/e2e-tests/manage.html'
EDIT_TEST_TEMPLATE = 'core_app/e2e-tests/edit.html'
DELETE_TEST_CONFIRM_TEMPLATE = 'core_app/e2e-tests/delete-confirm.html'



class CreateE2ETestView(LoginRequiredMixin, View):
    """Allow creating new tests.
    The class has two methods:
    GET - get a new empty form for creating new e2e-tests.
    POST - let the user create a new e2e-tests.
    """

    def get(self, request, *args, **kwargs):
        e2e_test_params__form = E2ETestParamsForm(request.GET or None)
        # On page load, reset the number of added forms
        e2e_test_action__formset = E2ETestActionFormsetCreate(queryset=E2ETestActionModel.objects.none())
        
        context = {
            'e2e_test_params__form': e2e_test_params__form,
            'e2e_test_action__formset': e2e_test_action__formset,
        }
        return render(request, CREATE_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # After creating a test, redirect to the page of managing all tests
        all_scheduled_tests = E2ETestParamsModel.objects.filter(user=request.user).order_by('-created')

        # Will be used to name the tests in the database with incremental numbers
        user_tests_count = E2ETestParamsModel.objects.filter(user=request.user).__len__()

        # Calculate form variables for the Celery task (& database storage)
        launches_per_day_raw = float(request.POST.get('launches_per_day'))
        # Prevent more than one test per minute
        launches_per_day_scaled_to_microseconds = 86400000000/max(round(launches_per_day_raw), 1)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=launches_per_day_scaled_to_microseconds,
            period=IntervalSchedule.MICROSECONDS,
        )

        # Create database-entry object
        e2e_test_params__form = E2ETestParamsForm(request.POST)
        e2e_test_action__formset = E2ETestActionFormsetCreateValidation(request.POST)

        # POST the entry to database
        if e2e_test_params__form.is_valid() and e2e_test_action__formset.is_valid():
            # Will be used to connect between the Celery task, PeriodicTask and crawler actions
            e2e_test_params = e2e_test_params__form.save(commit=False)
            # e2e_test_launches_in_minutes = (max(round(launches_per_day_scaled_to_microseconds), 1)/1000000)/60
            # new_e2e_test_job.launches_per_day = 1440/e2e_test_launches_in_minutes
            
            # Formset of crawler actions
            e2e_test_actions = []
            for form in e2e_test_action__formset:
                e2e_test_action = form.save(commit=False)
                e2e_test_action.e2e_test_params = e2e_test_params
                e2e_test_actions.append(e2e_test_action_form_to_dict(e2e_test_action))

            # Schedule the e2e-test using Celery
            periodic_task = PeriodicTask.objects.create(
                enabled = True if request.POST.get('enabled') == "on" else False,
                interval=schedule,
                name=str(request.user)+'_e2e-test_'+str(user_tests_count),
                task='core_app.tasks.call_crawl_website',
                start_time = request.POST.get('start_date'),
                expires = None if request.POST.get('end_date') == "" else request.POST.get('end_date'),
                one_off=False,
            )

            e2e_test_params.user = request.user
            e2e_test_params.launches_per_day = request.POST.get('launches_per_day')
            if type(request.POST.get('start_date')) is type(DateField):
                e2e_test_params.start_date = request.POST.get('start_date')
            if type(request.POST.get('end_date')) is type(DateField):
                e2e_test_params.end_date = request.POST.get('end_date')
            e2e_test_params.periodic_task = periodic_task
            e2e_test_params.save()

            # Update the PeriodicTask's parameters with the e2e-test instructions.
            # Must be after saving e2e_test_params to the database to get its pk.
            PeriodicTask.objects.filter(pk=periodic_task.pk).update(
                                kwargs=json.dumps({'user_pk': request.user.pk,
                                                   'e2e_test_params_pk': (e2e_test_params.pk),
                                                   'url': request.POST.get('url'), 
                                                   'tasks': e2e_test_actions,}),
                                                 )

            # Save last to prevent data-loss in previous forms
            for form in e2e_test_action__formset:
                form.save()

            messages.success(request, 'Created successfully.')
            # Clear the forms after a successful creation
            e2e_test_params__form = E2ETestParamsForm(request.GET or None)
            e2e_test_action__formset = E2ETestActionFormsetCreate(queryset=E2ETestActionModel.objects.none())
        else:
            messages.error(request, 'Please fix the issues below.')

        # Redirect to the page of managing all tests
        context = {
            'all_scheduled_tests': all_scheduled_tests,
        }

        return render(request, MANAGE_TESTS_TEMPLATE, context)



class ManageE2ETestsView(LoginRequiredMixin, View):
    """Render scheduled tests and allow creating new tests.
    GET - get all the scheduled e2e-tests.
    """
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Show all scheduled e2e-tests
        all_scheduled_tests = E2ETestParamsModel.objects.filter(user=request.user).order_by('-created')
        
        context = {
            'all_scheduled_tests': all_scheduled_tests,
        }
        return render(request, MANAGE_TESTS_TEMPLATE, context)



class EditE2ETestView(LoginRequiredMixin, View):
    """Render a scheduled test and allow to edit it.
    The class has two methods:
    GET - get a scheduled e2e-test.
    POST - let the user update parameters of the e2e-test.
    """

    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParamsModel.objects.get(pk=pk)
        # Latest actions should be last
        e2e_test_actions = E2ETestActionModel.objects.filter(e2e_test_params=e2e_test_params).order_by('-created').reverse()

        # instance=e2e_test_params will load the requested e2e-test form
        # with pre-filled fields.
        e2e_test_params__form = E2ETestParamsForm(instance=e2e_test_params)
        e2e_test_action__formset = E2ETestActionFormsetEditValidation(queryset=e2e_test_actions)

        context = {
            'e2e_test_params': e2e_test_params,
            'e2e_test_params__form': e2e_test_params__form,
            'e2e_test_actions': e2e_test_actions,
            'e2e_test_action__formset': e2e_test_action__formset,

        }
        return render(request, EDIT_TEST_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        """Update e2e-test settings.
        """
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_params_pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParamsModel.objects.get(pk=e2e_test_params_pk)
        
        # Calculate form variables for the Celery task (& database storage)
        launches_per_day_raw = float(request.POST.get('launches_per_day'))
        # Round to prevent more than one test per minute
        launches_per_day_scaled_to_microseconds = 86400000000/max(round(launches_per_day_raw), 1)
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=launches_per_day_scaled_to_microseconds,
            period=IntervalSchedule.MICROSECONDS,
        )

        # Create database-entry object
        e2e_test_params__form = E2ETestParamsForm(request.POST, instance=e2e_test_params) 
        e2e_test_action__formset = E2ETestActionFormsetEditValidation(request.POST)

        # POST the entry to database
        if e2e_test_params__form.is_valid() and e2e_test_action__formset.is_valid():
            # Will be used to connect between the Celery task, PeriodicTask and crawler actions
            e2e_test_params = e2e_test_params__form.save(commit=False)

            # Formset of crawler actions
            e2e_test_actions = []
            for form in e2e_test_action__formset:
                e2e_test_action = form.save(commit=False)
                e2e_test_action.e2e_test_params = e2e_test_params
                e2e_test_actions.append(e2e_test_action_form_to_dict(e2e_test_action))

            # Get the according Celery task from beat's PeriodicTask table
            periodic_task = PeriodicTask.objects.get(pk=e2e_test_params.periodic_task.id)
            # Update values in the Celery task
            periodic_task.enabled = True if request.POST.get('enabled') == "on" else False
            periodic_task.interval = schedule
            periodic_task.expires = None if request.POST.get('end_date') == "" else request.POST.get('end_date')
            periodic_task.kwargs = json.dumps({'user_pk': request.user.pk,
                                               'e2e_test_params_pk': e2e_test_params.pk,
                                               'url': request.POST.get('url'),
                                               'tasks': e2e_test_actions,})
            periodic_task.save()

            e2e_test_params.launches_per_day = request.POST.get('launches_per_day')
            if type(request.POST.get('start_date')) is type(DateField):
                e2e_test_params.start_date = request.POST.get('start_date')
            if type(request.POST.get('end_date')) is type(DateField):
                e2e_test_params.end_date = request.POST.get('end_date')
            e2e_test_params.save()
            
            # Save last to prevent data-loss in previous forms
            for form in e2e_test_action__formset:
                form.save()

            # Delete forms based on user-choice
            e2e_test_action__formset.save(commit=False)
            for form in e2e_test_action__formset.deleted_objects:
                form.delete()

            messages.success(request, 'Updated successfully.')
        else:
            messages.error(request, 'Please fix the issues below.')

        # Latest actions should be last
        e2e_test_actions = E2ETestActionModel.objects.filter(e2e_test_params=e2e_test_params).order_by('-created').reverse()
        e2e_test_params__form = E2ETestParamsForm(instance=e2e_test_params)
        e2e_test_action__formset = E2ETestActionFormsetEditValidation(queryset=e2e_test_actions)
        
        context = {
            'e2e_test_params': e2e_test_params,
            'e2e_test_params__form': e2e_test_params__form,
            'e2e_test_action__formset': e2e_test_action__formset
        }

        return render(request, EDIT_TEST_TEMPLATE, context)
    


class DeleteE2ETestView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_params_pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParamsModel.objects.get(pk=e2e_test_params_pk)

        context = {
            'e2e_test_params': e2e_test_params,
        }
        return render(request, DELETE_TEST_CONFIRM_TEMPLATE, context)

    def post(self, request, *args, **kwargs):
        # Get the chosen e2e-test with its current settings (fields)
        e2e_test_params_pk = self.kwargs.get('pk')
        e2e_test_params = E2ETestParamsModel.objects.get(pk=e2e_test_params_pk)
        # Get the according Celery task from beat's PeriodicTask table
        periodic_task = PeriodicTask.objects.get(pk=e2e_test_params.periodic_task.id)
        # Delete both
        e2e_test_params.delete()
        periodic_task.delete()

        # Return to the e2e tests' page
        return redirect(reverse('manage-e2e-tests'))



class E2ETestResultsListView(LoginRequiredMixin, generic.ListView):
    """List the results of the scheduled e2e-tests.
    """
    model = E2ETestResultsModel
    template_name = TEST_RESULTS_TEMPLATE
    paginate_by = 10

    def get_queryset(self):
        # Filter to the users' results
        qs = self.model.objects.filter(user=self.request.user)
        return qs