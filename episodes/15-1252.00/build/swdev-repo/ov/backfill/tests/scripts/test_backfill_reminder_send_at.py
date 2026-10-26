from datetime import date, datetime, timezone

from app.models import Invoice, InvoiceReminder, Tenant
from scripts.backfill_reminder_send_at import run

UTC = timezone.utc


def test_backfill_updates_only_wrong_scheduled_rows(engine, session):
    session.add_all([Tenant(id="ten_chi", name="Chicago", timezone="America/Chicago"),
                     Tenant(id="ten_phx", name="Phoenix", timezone="America/Phoenix")])
    session.flush()
    session.add_all([Invoice(id="in_1", tenant_id="ten_chi", due_date=date(2026, 11, 6)),
                     Invoice(id="in_2", tenant_id="ten_phx", due_date=date(2026, 11, 6))])
    session.flush()
    session.add_all([
        # scheduled in October with the CDT offset: 09:00 CDT = 14:00 UTC, should be 15:00 UTC
        InvoiceReminder(id=1, invoice_id="in_1", tenant_id="ten_chi", remind_on=date(2026, 11, 6),
                        send_at=datetime(2026, 11, 6, 14, 0, tzinfo=UTC)),
        # already correct
        InvoiceReminder(id=2, invoice_id="in_1", tenant_id="ten_chi", remind_on=date(2026, 11, 13),
                        send_at=datetime(2026, 11, 13, 15, 0, tzinfo=UTC)),
        # wrong but already sent: left alone
        InvoiceReminder(id=3, invoice_id="in_1", tenant_id="ten_chi", remind_on=date(2026, 11, 2),
                        send_at=datetime(2026, 11, 2, 14, 0, tzinfo=UTC), status="sent"),
        # Phoenix has no DST
        InvoiceReminder(id=4, invoice_id="in_2", tenant_id="ten_phx", remind_on=date(2026, 11, 6),
                        send_at=datetime(2026, 11, 6, 16, 0, tzinfo=UTC)),
    ])
    session.commit()

    assert run(engine, apply=False) == {"America/Chicago": 1}
    assert session.get(InvoiceReminder, 1).send_at.hour == 14  # dry run wrote nothing

    assert run(engine, apply=True) == {"America/Chicago": 1}
    session.expire_all()
    assert session.get(InvoiceReminder, 1).send_at == datetime(2026, 11, 6, 15, 0, tzinfo=UTC)
    assert session.get(InvoiceReminder, 3).send_at.hour == 14
    assert run(engine, apply=False) == {}  # idempotent
