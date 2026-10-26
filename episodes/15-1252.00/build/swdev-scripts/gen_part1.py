# Episode generator for 15-1252.00, part 1: helpers, world, incident data, code.
import difflib, json, random
from pathlib import Path

REPO = Path("/tmp/swdev-repo")
ITEMS, ACTIONS, CALLS = [], {1: [], 2: [], 3: [], 4: [], 5: []}, {1: [], 2: [], 3: [], 4: [], 5: []}


def src(rel, overlay=None):
    p = REPO / "ov" / overlay / rel if overlay else REPO / "base" / rel
    return p.read_text()


def diff(rel, old, new, new_file=False):
    a = [] if new_file else old.splitlines(keepends=True)
    b = new.splitlines(keepends=True)
    head = f"diff --git a/{rel} b/{rel}\n" + ("new file mode 100644\n" if new_file else "")
    body = "".join(difflib.unified_diff(a, b, "/dev/null" if new_file else f"a/{rel}", f"b/{rel}", n=3))
    return head + body


def item(id, channel, kind, at, thread, frm, to, subject, body, cc=None, attachments=None, meta=None):
    ITEMS.append(dict(id=id, channel=channel, kind=kind, at=at, thread=thread, **{"from": frm}, to=to or [],
                      cc=cc or [], subject=subject, body=body.strip("\n"), attachments=attachments or [],
                      meta=meta or {}))


def act(day, id, at, verb, target, content, note, visible=True):
    ACTIONS[day].append(dict(id=id, at=at, verb=verb, target=target, content=content.strip("\n"),
                             visible_to_model=visible, note=note))


# ---------------------------------------------------------------- incident data (INC-0412)
TENANTS = [  # id, name, invoice prefix, enabled endpoints, duplicated invoices
    ("ten_larkfield", "Larkfield Analytics", "LA", 2, 12),
    ("ten_ostrander", "Ostrander Field Services", "OFS", 1, 7),
    ("ten_tidelock", "Tidelock HR", "TL", 3, 5),
    ("ten_quenby", "Quenby Health Scheduling", "QHS", 1, 4),
    ("ten_velmora", "Velmora Learning", "VL", 0, 3),
    ("ten_brennanvale", "Brennanvale Freight", "BF", 2, 4),
    ("ten_quillon", "Quillon Data", "QD", 1, 2),
    ("ten_marrowgate", "Marrowgate Studios", "MS", 1, 2),
    ("ten_corriveau", "Corriveau IT", "CIT", 2, 2),
]
rng = random.Random(412)
rows = []
for tid, name, prefix, endpoints, n in TENANTS:
    num = rng.randint(300, 900)
    for k in range(n):
        num += rng.randint(1, 3)
        rows.append([tid, f"in_{rng.getrandbits(48):012x}", f"{prefix}-2026-{num:04d}"])
rng.shuffle(rows)
parallel = set(rng.sample(range(41), 14))
t = 16 * 3600 + 4 * 60 + 40  # 16:04:40 UTC = 10:04:40 CST
DUPS = []
for i, (tid, inv, num) in enumerate(rows):
    t += rng.randint(8, 34) if i else 0
    gap_ms = rng.randint(40, 700) if i in parallel else rng.randint(3000, 52000)
    DUPS.append((tid, inv, num, t + rng.randint(0, 999) / 1000, gap_ms))
assert len(DUPS) == 41 and len({d[2] for d in DUPS}) == 41 and len({d[1] for d in DUPS}) == 41
last_second = DUPS[-1][3] + DUPS[-1][4] / 1000


def hms(sec):
    sec = int(sec)
    return f"{sec // 3600:02d}:{sec % 3600 // 60:02d}:{sec % 60:02d}"


def stamp(sec_float):
    whole = int(sec_float)
    ms = int(round((sec_float - whole) * 1000))
    if ms == 1000:
        whole, ms = whole + 1, 0
    return f"2026-11-04 {hms(whole)}.{ms:03d}+00"


EP = {t[0]: t[3] for t in TENANTS}
NAME = {t[0]: t[1] for t in TENANTS}
DUP_DELIVERIES = sum(EP[d[0]] for d in DUPS)
N_TENANTS = len({d[0] for d in DUPS})
N_TENANTS_WITH_HOOKS = len({d[0] for d in DUPS if EP[d[0]] > 0})
N_PARALLEL = sum(1 for d in DUPS if d[4] < 1000)
LARKFIELD_NUMS = sorted(d[2] for d in DUPS if d[0] == "ten_larkfield")
assert (DUP_DELIVERIES, N_TENANTS, N_TENANTS_WITH_HOOKS, N_PARALLEL, len(LARKFIELD_NUMS)) == (66, 9, 8, 14, 12), (
    DUP_DELIVERIES, N_TENANTS, N_TENANTS_WITH_HOOKS, N_PARALLEL)
FIRST_DUP_CT = hms(DUPS[0][3] - 6 * 3600)
LAST_DUP_CT = hms(last_second - 6 * 3600)

dup_table = ["tenant_id        | invoice_id        | number        | first_created_at              | second_created_at             | events",
             "-----------------+-------------------+---------------+-------------------------------+-------------------------------+-------"]
for tid, inv, num, t0, gap in DUPS:
    dup_table.append(f"{tid:<16} | {inv:<17} | {num:<13} | {stamp(t0):<29} | {stamp(t0 + gap / 1000):<29} |      2")
dup_table.append(f"({len(DUPS)} rows)")
ep_table = ["tenant_id        | enabled_endpoints", "-----------------+------------------"]
for tid, *_ in TENANTS:
    ep_table.append(f"{tid:<16} | {EP[tid]:>17}")
ep_table.append(f"({len(TENANTS)} rows)")

# ---------------------------------------------------------------- reminder backfill numbers (Tomasz, Tue)
REM = [("America/New_York", 6842, 2311), ("America/Chicago", 3925, 1204), ("America/Los_Angeles", 3118, 876),
       ("Europe/London", 1487, 412), ("America/Denver", 604, 190), ("Europe/Berlin", 512, 151),
       ("Australia/Sydney", 298, 37), ("America/Phoenix", 233, 0), ("Asia/Kolkata", 141, 0), ("UTC", 96, 0)]
REM_PENDING, REM_WRONG = sum(r[1] for r in REM), sum(r[2] for r in REM)
assert (REM_PENDING, REM_WRONG) == (17256, 5181)
rem_table = ["timezone            | scheduled | wrong_send_at", "--------------------+-----------+--------------"]
for tz, p, w in REM:
    rem_table.append(f"{tz:<19} | {p:>9} | {w:>12}")
rem_table.append("(10 rows)")
BACKFILL_DRYRUN = 4862  # Thursday dry run: fewer rows, since reminders were sent Tue-Thu

# ---------------------------------------------------------------- code (exactly the files tested in /tmp/swdev-repo)
MODELS_MAIN = src("app/models.py")
cut = MODELS_MAIN.index("\n\nclass IdempotencyKey(Base):")
IDEM_MODEL = MODELS_MAIN[cut:]
MODELS_MAIN = MODELS_MAIN[:cut].rstrip("\n") + "\n"
MODELS_MAIN = MODELS_MAIN.replace(", UniqueConstraint", "")
SCHEDULE_MAIN = src("app/reminders/schedule.py")
SCHEDULE_TEST_MAIN = src("tests/reminders/test_schedule.py")
EMIT_MAIN = src("app/webhooks/emit.py")
DISPATCH_MAIN = src("app/webhooks/dispatch.py")
TASKS_MAIN = src("app/tasks.py")
FINALIZE_MAIN = '''"""Finalize a draft invoice: give it a number, open it, notify the tenant and the bill-to contact."""
from sqlalchemy import func

from app.db import session_scope
from app.invoices.numbering import next_invoice_number
from app.models import Invoice
from app.notifications.tasks import send_invoice_email
from app.tasks import celery_app
from app.webhooks.emit import emit_invoice_event


@celery_app.task(max_retries=5)
def finalize_invoice(invoice_id: str) -> None:
    with session_scope() as session:  # commits on exit
        invoice = session.get(Invoice, invoice_id, with_for_update=True)
        if invoice.status == "draft":
            invoice.number = next_invoice_number(session, invoice.tenant_id)
            invoice.status = "open"
            invoice.finalized_at = func.now()
    with session_scope() as session:
        emit_invoice_event(session, session.get(Invoice, invoice_id), "invoice.finalized")
    send_invoice_email.delay(invoice_id)
'''
LOCK_EXCERPT = '''# requirements.lock (excerpt; generated by pip-compile --generate-hashes, hashes omitted here)
alembic==1.20.1
boto3==1.43.112
botocore==1.43.112
    # via boto3, s3transfer
celery[redis]==5.6.3
fastapi==0.161.1
kombu==5.6.2
psycopg[binary]==3.3.6
pydantic==2.14.1
pyjwt==2.15.1
redis==6.4.0
requests==2.34.2
sentry-sdk==2.41.0
sqlalchemy==2.1.5
starlette==1.8.0
urllib3==2.7.0
    # via botocore, requests, sentry-sdk
'''
CODEOWNERS = '''# .github/CODEOWNERS (excerpt)
*                         @cobaltline/invoicing
/migrations/              @cobaltline/invoicing @cobaltline/platform-db
/app/billing/tax/         @cobaltline/invoicing @cobaltline/finance-eng
/.github/workflows/       @cobaltline/platform
'''

IDEM_FRI = src("app/api/idempotency.py", "pr1487_fri")
IDEM_MON = src("app/api/idempotency.py", "pr1487_mon")
IDEM_REF = src("app/api/idempotency.py", "pr1487_ref")
IDEM_T_FRI = src("tests/api/test_idempotency.py", "pr1487_fri")
IDEM_T_MON = src("tests/api/test_idempotency.py", "pr1487_mon")
IDEM_T_REF = src("tests/api/test_idempotency.py", "pr1487_ref")
MIG_1487 = src("migrations/versions/20261029_1412_add_idempotency_keys.py", "pr1487_fri")
PRO_V1 = src("app/billing/proration.py", "pr1490_v1")
PRO_T_V1 = src("tests/billing/test_proration.py", "pr1490_v1")
PRO_REF = src("app/billing/proration.py", "pr1490_ref")
PRO_T_REF = src("tests/billing/test_proration.py", "pr1490_ref")
SCHED_FIX = src("app/reminders/schedule.py", "pr1494")
SCHED_T_FIX = src("tests/reminders/test_schedule.py", "pr1494")
BACKFILL = src("scripts/backfill_reminder_send_at.py", "backfill")
BACKFILL_T = src("tests/scripts/test_backfill_reminder_send_at.py", "backfill")
EMIT_V1 = src("app/webhooks/emit.py", "pr1495_v1")
EMIT_V2 = src("app/webhooks/emit.py", "pr1495_v2")
EMIT_T_V2 = src("tests/webhooks/test_emit.py", "pr1495_v2")
EMIT_T_REF = src("tests/webhooks/test_emit.py", "pr1495_ref")
MIG_1495_V2 = src("migrations/versions/20261104_1431_webhook_events_dedupe_key.py", "pr1495_v2")
MIG_1495_REF = src("migrations/versions/20261104_1431_webhook_events_dedupe_key.py", "pr1495_ref")
MODELS_DEDUPE_LINE = "    dedupe_key: Mapped[str | None] = mapped_column(Text, unique=True)  # set only for ONCE_PER_INVOICE types\n"

D_1487_FRI = "\n".join([
    diff("app/api/idempotency.py", "", IDEM_FRI, True),
    diff("app/models.py", MODELS_MAIN, MODELS_MAIN.replace("from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func",
         "from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func") + IDEM_MODEL.lstrip("\n").join(["\n\n", ""])),
    diff("migrations/versions/20261029_1412_add_idempotency_keys.py", "", MIG_1487, True),
    diff("tests/api/test_idempotency.py", "", IDEM_T_FRI, True)])
D_1487_MON = "\n".join([diff("app/api/idempotency.py", IDEM_FRI, IDEM_MON), diff("tests/api/test_idempotency.py", IDEM_T_FRI, IDEM_T_MON)])
D_1487_REF = "\n".join([diff("app/api/idempotency.py", IDEM_MON, IDEM_REF), diff("tests/api/test_idempotency.py", IDEM_T_MON, IDEM_T_REF)])
D_1490_V1 = "\n".join([diff("app/billing/proration.py", "", PRO_V1, True), diff("tests/billing/test_proration.py", "", PRO_T_V1, True)])
D_1490_V2 = "\n".join([diff("app/billing/proration.py", PRO_V1, PRO_REF), diff("tests/billing/test_proration.py", PRO_T_V1, PRO_T_REF)])
D_1494 = "\n".join([diff("app/reminders/schedule.py", SCHEDULE_MAIN, SCHED_FIX), diff("tests/reminders/test_schedule.py", SCHEDULE_TEST_MAIN, SCHED_T_FIX)])
D_1497 = "\n".join([diff("scripts/backfill_reminder_send_at.py", "", BACKFILL, True),
                    diff("tests/scripts/test_backfill_reminder_send_at.py", "", BACKFILL_T, True)])
D_1495_V1 = diff("app/webhooks/emit.py", EMIT_MAIN, EMIT_V1)
models_dd = MODELS_MAIN.replace("    payload: Mapped[dict] = mapped_column(JSONB)\n", "    payload: Mapped[dict] = mapped_column(JSONB)\n" + MODELS_DEDUPE_LINE)
D_1495_V2 = "\n".join([diff("app/webhooks/emit.py", EMIT_V1, EMIT_V2), diff("app/models.py", MODELS_MAIN, models_dd),
                       diff("migrations/versions/20261104_1431_webhook_events_dedupe_key.py", "", MIG_1495_V2, True),
                       diff("tests/webhooks/test_emit.py", "", EMIT_T_V2, True)])
D_1495_V3 = "\n".join([diff("migrations/versions/20261104_1431_webhook_events_dedupe_key.py", MIG_1495_V2, MIG_1495_REF),
                       diff("tests/webhooks/test_emit.py", EMIT_T_V2, EMIT_T_REF)])

MIG_1487_REBASED = MIG_1487.replace('Revises: 5f3b2d8e61aa', 'Revises: 9a4d2c7e1f05').replace(
    'down_revision = "5f3b2d8e61aa"', 'down_revision = "9a4d2c7e1f05"  # rebased on INC-0412\'s dedupe_key migration')
assert MIG_1487_REBASED.count("9a4d2c7e1f05") == 2
D_1487_REF = D_1487_REF + "\n" + diff("migrations/versions/20261029_1412_add_idempotency_keys.py", MIG_1487, MIG_1487_REBASED)
