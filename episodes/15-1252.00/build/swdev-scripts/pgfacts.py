import importlib.util, threading, time
import sqlalchemy as sa
from alembic.migration import MigrationContext
from alembic.operations import Operations

URL = "postgresql+psycopg://postgres:@/postgres?host=/tmp/swdev-pgdata"
eng = sa.create_engine(URL)
with eng.begin() as c:
    c.execute(sa.text("DROP SCHEMA IF EXISTS facts CASCADE; CREATE SCHEMA facts; SET search_path=facts"))
    c.execute(sa.text("CREATE TABLE facts.webhook_events (id text primary key, invoice_id text, type text)"))
    c.execute(sa.text("INSERT INTO facts.webhook_events SELECT 'evt_'||g, 'in_'||(g/2), 'invoice.finalized' FROM generate_series(1,400000) g"))

# 1. lock taken by plain CREATE INDEX, and an INSERT from another session blocking on it
holder = eng.connect(); holder.execute(sa.text("BEGIN"))
holder.execute(sa.text("CREATE INDEX ix_plain ON facts.webhook_events (invoice_id)"))
with eng.connect() as obs:
    modes = obs.execute(sa.text("SELECT mode FROM pg_locks l JOIN pg_class c ON c.oid=l.relation WHERE c.relname='webhook_events' AND l.pid <> pg_backend_pid()")).scalars().all()
    print("1. locks held by CREATE INDEX txn:", modes)
    obs.execute(sa.text("SET lock_timeout='200ms'"))
    try:
        obs.execute(sa.text("INSERT INTO facts.webhook_events VALUES ('evt_x','in_x','invoice.finalized')"))
        print("   insert succeeded")
    except Exception as e:
        print("   insert during plain CREATE INDEX ->", type(e.orig).__name__, str(e.orig).splitlines()[0])
holder.execute(sa.text("ROLLBACK")); holder.close()

# 2. CONCURRENTLY inside a transaction block
with eng.connect() as c:
    try:
        c.execute(sa.text("BEGIN")); c.execute(sa.text("CREATE INDEX CONCURRENTLY ix_c ON facts.webhook_events (invoice_id)"))
    except Exception as e:
        print("2. CONCURRENTLY in txn ->", str(e.orig).splitlines()[0])

# 3. unique index on (invoice_id, type) fails because of existing duplicate pairs
with eng.connect() as c:
    try:
        c.execute(sa.text("CREATE UNIQUE INDEX uq_pair ON facts.webhook_events (invoice_id, type)")); c.commit()
    except Exception as e:
        print("3. unique (invoice_id,type) on existing dupes ->", str(e.orig).splitlines()[0])

# 4. run the reference migration through Alembic (autocommit_block + postgresql_concurrently)
spec = importlib.util.spec_from_file_location("mig", "/tmp/swdev-repo/ov/pr1495_ref/migrations/versions/20261104_1431_webhook_events_dedupe_key.py")
mig = importlib.util.module_from_spec(spec); spec.loader.exec_module(mig)
with eng.connect() as conn:
    conn.execute(sa.text("SET search_path=facts")); conn.commit()
    ctx = MigrationContext.configure(conn, opts={"transactional_ddl": True})
    with Operations.context(ctx):
        with ctx.begin_transaction():
            mig.upgrade()
with eng.connect() as c:
    print("4. after ref migration:", c.execute(sa.text("SELECT indexdef FROM pg_indexes WHERE schemaname='facts' AND indexname='uq_webhook_events_dedupe_key'")).scalar())
    print("   valid:", c.execute(sa.text("SELECT indisvalid FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid WHERE c.relname='uq_webhook_events_dedupe_key'")).scalar())
    c.execute(sa.text("SET search_path=facts"))
    c.execute(sa.text("INSERT INTO webhook_events (id, invoice_id, type) VALUES ('evt_n1','in_1','invoice.payment_failed'),('evt_n2','in_1','invoice.payment_failed')"))
    print("   two NULL dedupe_key rows inserted fine (NULLs distinct)")
    c.rollback()

# 5. Tomasz's query expression: (date + time) AT TIME ZONE tz
with eng.connect() as c:
    for tz, d in [("America/Chicago","2026-11-02"),("America/Chicago","2026-10-30"),("Europe/London","2026-11-02"),("Australia/Sydney","2026-10-02"),("America/Phoenix","2026-11-02")]:
        v = c.execute(sa.text("SELECT ((CAST(:d AS date) + time '09:00') AT TIME ZONE :tz) AT TIME ZONE 'UTC'"), {"d": d, "tz": tz}).scalar()
        print("5.", tz, d, "-> UTC", v)
with eng.begin() as c:
    c.execute(sa.text("DROP SCHEMA facts CASCADE"))
