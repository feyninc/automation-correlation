"""Idempotency-Key support for POST /v1/invoices (INV-2291).

Status codes follow draft-ietf-httpapi-idempotency-key-header: 400 if the key is
missing or malformed, 422 if a key is reused with a different body, 409 while the
first request with the key is still being processed.
"""
import hashlib
import json
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models import IdempotencyKey

KEY_TTL = timedelta(hours=24)  # rows are deleted by the hourly purge_idempotency_keys task
MAX_KEY_LENGTH = 255


def fingerprint(body: dict) -> str:
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


def begin(session: Session, tenant_id: str, key: str | None, body: dict) -> IdempotencyKey | None:
    """Claim the key for this request (returns None) or return the stored record to replay."""
    if not key or len(key) > MAX_KEY_LENGTH:
        raise HTTPException(400, "Idempotency-Key header must be 1-255 characters")
    request_hash = fingerprint(body)
    claimed = session.scalar(
        insert(IdempotencyKey)
        .values(
            tenant_id=tenant_id,
            key=key,
            request_hash=request_hash,
            expires_at=datetime.now(timezone.utc) + KEY_TTL,
        )
        .on_conflict_do_nothing(constraint="uq_idempotency_keys_tenant_key")
        .returning(IdempotencyKey.id)
    )
    session.commit()
    if claimed is not None:
        return None
    record = session.scalar(
        select(IdempotencyKey).where(IdempotencyKey.tenant_id == tenant_id, IdempotencyKey.key == key)
    )
    if record.request_hash != request_hash:
        raise HTTPException(422, "Idempotency-Key was already used with a different request body")
    if record.response_status is None:
        raise HTTPException(409, "A request with this Idempotency-Key is still being processed")
    return record


def complete(session: Session, tenant_id: str, key: str, status: int, body: dict) -> None:
    """Store the response so retries replay it."""
    record = session.scalar(
        select(IdempotencyKey).where(IdempotencyKey.tenant_id == tenant_id, IdempotencyKey.key == key)
    )
    record.response_status = status
    record.response_body = body
    session.commit()
