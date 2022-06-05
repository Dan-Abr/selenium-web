from django.views import generic
from .models import CrawlerResults

class DOMElementListView(generic.ListView):
    model = CrawlerResults
    template_name = "dom_elements_list.html"


