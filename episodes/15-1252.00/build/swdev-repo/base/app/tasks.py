"""Celery tasks (excerpt). Broker: ElastiCache Redis; task_acks_late=True for every task."""
from celery import Celery

celery_app = Celery("billing")
celery_app.conf.task_acks_late = True


@celery_app.task(max_retries=8)
def deliver_webhook(event_id: str, endpoint_id: str) -> None:
    from app.webhooks.dispatch import deliver

    deliver(event_id, endpoint_id)
