from datetime import date

import pytest

from app.models import Invoice, Tenant, WebhookEndpoint, WebhookEvent
from app.webhooks import emit


@pytest.fixture
def queued(monkeypatch):
    calls = []
    monkeypatch.setattr(emit.deliver_webhook, "delay", lambda *args: calls.append(args))
    return calls


@pytest.fixture
def invoice(session):
    session.add(Tenant(id="ten_a", name="Tenant A", timezone="UTC"))
    session.flush()
    session.add_all([WebhookEndpoint(id="we_1", tenant_id="ten_a", url="https://a.example/hooks"),
                     WebhookEndpoint(id="we_2", tenant_id="ten_a", url="https://a.example/erp")])
    inv = Invoice(id="in_1", tenant_id="ten_a", status="open", number="A-0042", total_cents=49900,
                  due_date=date(2026, 12, 4))
    session.add(inv)
    session.commit()
    return inv


def test_emit_invoice_event_twice_creates_one_event(session, invoice, queued):
    assert emit.emit_invoice_event(session, invoice, "invoice.finalized") is not None
    assert emit.emit_invoice_event(session, invoice, "invoice.finalized") is None
    assert session.query(WebhookEvent).count() == 1
    assert len(queued) == 2  # one delivery per endpoint, once
