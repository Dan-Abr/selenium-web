from django.views import generic
from .models import CrawlerTask

class DOMElementListView(generic.ListView):
    model = CrawlerTask
    template_name = "dom_elements_list.html"


