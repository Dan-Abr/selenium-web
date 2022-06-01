from django.views import generic
from .models import DOMElement

class DOMElementListView(generic.ListView):
    model = DOMElement
    template_name = "dom_elements_list.html"


