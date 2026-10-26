"""Recompute send_at for scheduled reminders stored with the wrong UTC offset (INV-2312).

Reminders scheduled before a DST change kept the offset in force when they were
scheduled. This recomputes every scheduled reminder from (remind_on, tenant timezone)
with the fixed reminder_send_at and updates only the rows that differ.

    python -m scripts.backfill_reminder_send_at            # dry run: prints counts per zone
    python -m scripts.backfill_reminder_send_at --apply    # writes, 1,000 rows per transaction

Each changed row is first copied to reminder_send_at_backfill (id, old, new) so the
change can be reverted with one UPDATE ... FROM.
"""
import argparse
from collections import Counter

from sqlalchemy import Engine, create_engine, text

from app.reminders.schedule import reminder_send_at

BATCH = 1000

SELECT_SCHEDULED = text("""
    SELECT r.id, r.remind_on, t.timezone, r.send_at
    FROM invoice_reminders r JOIN tenants t ON t.id = r.tenant_id
    WHERE r.status = 'scheduled' AND r.id > :after
    ORDER BY r.id
    LIMIT :limit
""")


def plan_updates(rows):
    """rows: (id, remind_on, tz_name, send_at). Yields (id, tz_name, old, new) for rows that differ."""
    for reminder_id, remind_on, tz_name, send_at in rows:
        new = reminder_send_at(remind_on, tz_name)
        if new != send_at:
            yield reminder_id, tz_name, send_at, new


def run(engine: Engine, apply: bool) -> Counter:
    changed: Counter = Counter()
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE IF NOT EXISTS reminder_send_at_backfill "
            "(id integer PRIMARY KEY, old_send_at timestamptz NOT NULL, new_send_at timestamptz NOT NULL)"
        ))
    after = 0
    while True:
        with engine.begin() as conn:
            rows = conn.execute(SELECT_SCHEDULED, {"after": after, "limit": BATCH}).all()
            if not rows:
                return changed
            after = rows[-1][0]
            updates = list(plan_updates(rows))
            changed.update(tz for _, tz, _, _ in updates)
            if apply and updates:
                params = [{"id": i, "old": old, "new": new} for i, _, old, new in updates]
                conn.execute(text(
                    "INSERT INTO reminder_send_at_backfill VALUES (:id, :old, :new) ON CONFLICT (id) DO NOTHING"
                ), params)
                conn.execute(text(
                    "UPDATE invoice_reminders SET send_at = :new "
                    "WHERE id = :id AND status = 'scheduled' AND send_at = :old"
                ), params)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--database-url", required=True)
    args = parser.parse_args()
    counts = run(create_engine(args.database_url), apply=args.apply)
    for tz, n in counts.most_common():
        print(f"{tz:24} {n:6}")
    print(f"{'total':24} {sum(counts.values()):6}  ({'applied' if args.apply else 'dry run'})")
