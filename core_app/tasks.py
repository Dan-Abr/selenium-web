# third-party
from celery import Celery, shared_task

# local Django
from .crawlers import crawl_website


app = Celery('tasks', broker='redis://localhost/', backend='redis://localhost/')
# celery -A selenium_web beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A selenium_web beat --loglevel=info


@shared_task
def call_crawl_website(user_pk=None, e2e_test_pk=None, url="", tasks=None):
    if user_pk == None or e2e_test_pk == None or tasks == None:
        # Must belong to an active user.
        # Must belong to existing e2e-test.
        # Must have tasks to do in the website.
        return
    crawl_website(user_pk, e2e_test_pk, url, tasks)
    return