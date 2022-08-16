# third-party
from celery import Celery, shared_task

# local Django
from .crawlers import crawl_website


app = Celery('tasks', broker='redis://localhost/', backend='redis://localhost/')
# celery -A selenium_web beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
# celery -A selenium_web beat --loglevel=info


@shared_task
def call_crawl_website(user_pk=None, e2e_test_params_pk=None, url=None, tasks=None):
    if user_pk == None or e2e_test_params_pk == None or url == None or tasks == None:
        # Must belong to an active user.
        # Must belong to existing e2e-test.
        # Must have tasks to do in the website.

        # Raise error
        return
    crawl_website(user_pk, e2e_test_params_pk, url, tasks)
    return