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


def test_payment_failed_events_are_not_deduplicated(session, invoice, queued):
    emit.emit_invoice_event(session, invoice, "invoice.payment_failed")
    emit.emit_invoice_event(session, invoice, "invoice.payment_failed")
    assert session.query(WebhookEvent).filter_by(type="invoice.payment_failed").count() == 2


def test_concurrent_emits_create_one_event(engine, session, invoice, queued):
    """Two runs of the task in parallel (Celery redelivery on broker connection loss)."""
    import threading

    from sqlalchemy.orm import Session

    results, barrier = [], threading.Barrier(2)

    def run():
        with Session(engine) as s:
            inv = s.get(Invoice, "in_1")
            barrier.wait()
            results.append(emit.emit_invoice_event(s, inv, "invoice.finalized"))

    threads = [threading.Thread(target=run) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(r is None for r in results) == [False, True]
    assert session.query(WebhookEvent).count() == 1
