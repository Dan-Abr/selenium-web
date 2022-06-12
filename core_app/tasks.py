# third-party
from celery import Celery, shared_task

# local Django
from .crawlers import crawl_website


app = Celery('tasks', broker='redis://localhost/', backend='redis://localhost/')
# celery -A selenium_web beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A selenium_web beat --loglevel=info


find_element_class = "//div[@class='A8SBwf']"
@shared_task
def call_crawl_website(url="", css_selector=find_element_class): # +number tests param
    crawl_website(url, css_selector)
    return