import os
from django.conf import settings
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery(
    "app", broker=settings.REDIS_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)

# app.config_from_object("django.conf:settings")
app.conf.task_routes = (
    [
        (
            "ops.tasks.anomalyDetectionTasks._anomalyDetectionSubTask",
            {"queue": "anomalySubTask"},
        ),
        ("ops.tasks.telemetryTask.telemetryJob", {"queue": "telemetry"}),
    ],
)


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    """
    Celery debug task
    """
    print(f"Request: {self.request!r}")
