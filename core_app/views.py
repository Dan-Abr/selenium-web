from django.shortcuts import redirect, render
from django.views import View, generic

from .forms import E2ETestParamsForm
from .models import E2ETestParams, E2ETestResults

TEST_RESULTS_TEMPLATE = 'pages/test_results_list.html'
ADD_TEST_TEMPLATE = 'pages/add-test.html'

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
    GET - get all scheduled tests.
    POST - let the user add new tests.
    """

    def get(self, request, *args, **kwargs):
        # Show all scheduled tests
        scheduled_tests = E2ETestParams.objects.filter().order_by('-created')
        add_test_form = E2ETestParamsForm

        context = {
            'scheduled tests': scheduled_tests,
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

        context = {
            'scheduled tests': scheduled_tests,
            'add_test_form': add_test_form,
        }

        return render(request, ADD_TEST_TEMPLATE, context)
