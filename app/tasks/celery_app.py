from celery import Celery
 
from app.core.config import settings


celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.example"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,               # Only ack after task completes
    worker_prefetch_multiplier=1,       # Fair task distribution
    beat_schedule={
        # Example scheduled task — runs every 60 seconds
        # "example-task": {
        #     "task": "app.tasks.example.example_task",
        #     "schedule": 60.0,
        # },
    },
)