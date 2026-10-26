"""Record webhook events and queue their deliveries."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ids import new_id
from app.models import Invoice, WebhookEndpoint, WebhookEvent
from app.tasks import deliver_webhook
from app.webhooks.payloads import invoice_payload


def emit_invoice_event(session: Session, invoice: Invoice, event_type: str) -> str:
    """Record one event for the invoice and queue a delivery to each enabled endpoint."""
    event = WebhookEvent(
        id=new_id("evt"),
        tenant_id=invoice.tenant_id,
        invoice_id=invoice.id,
        type=event_type,
        payload=invoice_payload(invoice),
    )
    session.add(event)
    endpoint_ids = session.scalars(
        select(WebhookEndpoint.id).where(
            WebhookEndpoint.tenant_id == invoice.tenant_id, WebhookEndpoint.enabled.is_(True)
        )
    ).all()
    session.commit()
    for endpoint_id in endpoint_ids:
        deliver_webhook.delay(event.id, endpoint_id)
    return event.id
