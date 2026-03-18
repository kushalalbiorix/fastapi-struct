import logging

from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_welcome_email(self, user_id: str, email: str) -> dict:
    """
    Send a welcome email to a new user.
    Retries up to 3 times with 60s delay on failure.
    """
    try:
        logger.info("Sending welcome email to %s (user_id=%s)", email, user_id)
        # TODO: integrate with your email provider (SendGrid, SES, Resend, etc.)
        return {"status": "sent", "user_id": user_id, "email": email}
    except Exception as exc:
        logger.exception("Failed to send welcome email to %s", email)
        raise self.retry(exc=exc)


@celery_app.task
def example_task() -> str:
    """Scheduled example task wired to Celery Beat."""
    logger.info("Running scheduled example task")
    return "ok"