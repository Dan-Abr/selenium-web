from django.views import generic
from .models import CrawlerResults

CRAWLER_RESULTS_TEMPLATE = 'layout/crawler_results_list.html'

class CrawlerResultsListView(generic.ListView):
    model = CrawlerResults
    template_name = CRAWLER_RESULTS_TEMPLATE
    paginate_by = 10


