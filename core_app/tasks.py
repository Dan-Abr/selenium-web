# third-party
from celery import Celery, shared_task

# local Django
from .crawlers import crawl_website


app = Celery('tasks', broker='redis://localhost/', backend='redis://localhost/')


@shared_task
def call_crawl_website(user_pk=None, e2e_test_params_pk=None, url=None, tasks=None):
    if user_pk == None:
        # Must belong to an active user.
        raise TypeError('user_pk cannot be null')
    elif e2e_test_params_pk == None:
        # Must belong to existing e2e-test.
        raise TypeError('e2e_test_params_pk cannot be null')
    elif url == None:
        # Must have a valid URL.
        raise TypeError('URL cannot be null')
    elif tasks == None:
        #  Must have tasks to do in the website.
        raise TypeError('tasks cannot be null')
    
    # Everything is fine, call the crawler.
    crawl_website(user_pk, e2e_test_params_pk, url, tasks)
    return