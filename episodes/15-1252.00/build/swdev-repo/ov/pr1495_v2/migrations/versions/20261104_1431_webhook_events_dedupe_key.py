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
    op.add_column("webhook_events", sa.Column("dedupe_key", sa.Text(), nullable=True))
    op.create_index("uq_webhook_events_dedupe_key", "webhook_events", ["dedupe_key"], unique=True)


def downgrade() -> None:
    op.drop_index("uq_webhook_events_dedupe_key", table_name="webhook_events")
    op.drop_column("webhook_events", "dedupe_key")
