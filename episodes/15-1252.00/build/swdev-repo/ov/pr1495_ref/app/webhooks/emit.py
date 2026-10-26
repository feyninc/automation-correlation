"""Record webhook events and queue their deliveries."""
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.ids import new_id
from app.models import Invoice, WebhookEndpoint, WebhookEvent
from app.tasks import deliver_webhook
from app.webhooks.payloads import invoice_payload

# Events that happen at most once in an invoice's life. Others (invoice.payment_failed,
# invoice.updated, ...) can legitimately repeat and are never deduplicated.
ONCE_PER_INVOICE = frozenset({"invoice.finalized", "invoice.paid", "invoice.voided"})


def emit_invoice_event(session: Session, invoice: Invoice, event_type: str) -> str | None:
    """Record the event and queue a delivery to each enabled endpoint.

    Returns None, and queues nothing, if this once-per-invoice event was already
    recorded (a redelivered or concurrent run of the same task, INC-0412).
    """
    dedupe_key = f"{invoice.id}:{event_type}" if event_type in ONCE_PER_INVOICE else None
    event_id = session.scalar(
        insert(WebhookEvent)
        .values(
            id=new_id("evt"),
            tenant_id=invoice.tenant_id,
            invoice_id=invoice.id,
            type=event_type,
            payload=invoice_payload(invoice),
            dedupe_key=dedupe_key,
        )
        .on_conflict_do_nothing(index_elements=["dedupe_key"])
        .returning(WebhookEvent.id)
    )
    if event_id is None:
        session.commit()
        return None
    endpoint_ids = session.scalars(
        select(WebhookEndpoint.id).where(
            WebhookEndpoint.tenant_id == invoice.tenant_id, WebhookEndpoint.enabled.is_(True)
        )
    ).all()
    session.commit()
    for endpoint_id in endpoint_ids:
        deliver_webhook.delay(event_id, endpoint_id)
    return event_id
