"""When to send an invoice's payment reminders."""
from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

REMINDER_LOCAL_TIME = time(9, 0)  # 09:00 in the tenant's time zone


def reminder_send_at(remind_on: date, tz_name: str, now: datetime | None = None) -> datetime:
    """Return the UTC instant to send a reminder: 09:00 tenant-local on remind_on."""
    now = now or datetime.now(timezone.utc)
    offset = now.astimezone(ZoneInfo(tz_name)).utcoffset()
    local = datetime.combine(remind_on, REMINDER_LOCAL_TIME)
    return (local - offset).replace(tzinfo=timezone.utc)
