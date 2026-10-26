"""When to send an invoice's payment reminders."""
from datetime import date, datetime, time, timezone
from zoneinfo import ZoneInfo

REMINDER_LOCAL_TIME = time(9, 0)  # 09:00 in the tenant's time zone


def reminder_send_at(remind_on: date, tz_name: str) -> datetime:
    """Return the UTC instant to send a reminder: 09:00 tenant-local on remind_on.

    The UTC offset is the one in force on remind_on, not today's, so reminders
    scheduled before a DST change still go out at 09:00 local after it.
    """
    local = datetime.combine(remind_on, REMINDER_LOCAL_TIME, tzinfo=ZoneInfo(tz_name))
    return local.astimezone(timezone.utc)
