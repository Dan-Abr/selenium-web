from celery import Celery, shared_task, task

app = Celery('tasks', broker='redis://localhost/', backend='redis://localhost/')

@shared_task
def add(x, y):
    return x+y
