from celery import Celery, shared_task
from crawlers import crawl_website

app = Celery("tasks", broker="redis://localhost/", backend="redis://localhost/")

@shared_task
def add(x, y):
    return x+y

@shared_task
def crawl_google():
    crawl_website("https://google.com")
    return