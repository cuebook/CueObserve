import os
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery(
    "app", broker=settings.REDIS_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

# app.config_from_object("django.conf:settings")
app.conf.task_routes = settings.CELERY_TASK_ROUTES

app.conf.task_acks_late = settings.CELERY_TASKS_ACKS_LATE
app.conf.worker_prefetch_multiplier = settings.CELERY_WORKER_PREFETCH_MULTIPLIER

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Celery debug task
    """
    print(f"Request: {self.request!r}")
