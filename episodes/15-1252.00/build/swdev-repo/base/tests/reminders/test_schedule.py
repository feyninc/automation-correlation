from datetime import date, datetime, timezone

from app.reminders.schedule import reminder_send_at


def test_reminder_send_at_is_nine_local():
    now = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
    assert reminder_send_at(date(2026, 7, 15), "America/Chicago", now=now) == datetime(
        2026, 7, 15, 14, 0, tzinfo=timezone.utc
    )


def test_reminder_send_at_utc_tenant():
    now = datetime(2026, 7, 1, 12, 0, tzinfo=timezone.utc)
    assert reminder_send_at(date(2026, 7, 15), "UTC", now=now) == datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)
