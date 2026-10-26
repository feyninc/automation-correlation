"""webhook_events.dedupe_key (INC-0412)

Revision ID: 9a4d2c7e1f05
Revises: 5f3b2d8e61aa
Create Date: 2026-11-04 14:31:52
"""
import sqlalchemy as sa
from alembic import op

revision = "9a4d2c7e1f05"
down_revision = "5f3b2d8e61aa"


def upgrade() -> None:
    op.execute("SET LOCAL lock_timeout = '5s'")  # add_column only: fail fast, don't queue writes behind it
    op.add_column("webhook_events", sa.Column("dedupe_key", sa.Text(), nullable=True))  # metadata-only
    # A plain CREATE INDEX holds a SHARE lock (no INSERTs) for the whole build of ~38M rows.
    # CONCURRENTLY cannot run inside a transaction, hence the autocommit block.
    with op.get_context().autocommit_block():
        op.create_index(
            "uq_webhook_events_dedupe_key",
            "webhook_events",
            ["dedupe_key"],
            unique=True,
            postgresql_concurrently=True,
        )


def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.drop_index("uq_webhook_events_dedupe_key", table_name="webhook_events", postgresql_concurrently=True)
    op.drop_column("webhook_events", "dedupe_key")
