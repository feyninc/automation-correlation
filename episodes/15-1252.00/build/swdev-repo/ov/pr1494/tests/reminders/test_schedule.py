from datetime import date, datetime, timezone

import pytest

from app.reminders.schedule import reminder_send_at


def test_reminder_send_at_is_nine_local():
    assert reminder_send_at(date(2026, 7, 15), "America/Chicago") == datetime(2026, 7, 15, 14, 0, tzinfo=timezone.utc)


def test_reminder_send_at_utc_tenant():
    assert reminder_send_at(date(2026, 7, 15), "UTC") == datetime(2026, 7, 15, 9, 0, tzinfo=timezone.utc)


@pytest.mark.parametrize(
    "remind_on, tz_name, expected_utc_hour",
    [
        (date(2026, 10, 30), "America/Chicago", 14),  # CDT, UTC-5
        (date(2026, 11, 2), "America/Chicago", 15),  # CST, UTC-6 (DST ended 2026-11-01)
        (date(2026, 11, 2), "Europe/London", 9),  # GMT (BST ended 2026-10-25)
        (date(2026, 10, 2), "Australia/Sydney", 23),  # AEST, 09:00 local is 23:00 UTC the day before
        (date(2026, 11, 2), "America/Phoenix", 16),  # no DST
    ],
)
def test_reminder_send_at_uses_offset_of_remind_on(remind_on, tz_name, expected_utc_hour):
    assert reminder_send_at(remind_on, tz_name).hour == expected_utc_hour
