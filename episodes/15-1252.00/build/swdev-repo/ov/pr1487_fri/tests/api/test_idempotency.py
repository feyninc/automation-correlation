import pytest
from fastapi import HTTPException

from app.api import idempotency
from app.models import Tenant

BODY = {"customer": "cus_123", "lines": [{"price": "price_pro", "quantity": 1}]}


@pytest.fixture
def tenant(session):
    session.add(Tenant(id="ten_a", name="Tenant A", timezone="UTC"))
    session.commit()
    return "ten_a"


def test_first_request_claims_key(session, tenant):
    assert idempotency.begin(session, tenant, "k1", BODY) is None


def test_retry_replays_stored_response(session, tenant):
    idempotency.begin(session, tenant, "k1", BODY)
    idempotency.complete(session, tenant, "k1", 201, {"id": "in_1"})
    record = idempotency.begin(session, tenant, "k1", BODY)
    assert (record.response_status, record.response_body) == (201, {"id": "in_1"})


def test_same_key_different_body_is_422(session, tenant):
    idempotency.begin(session, tenant, "k1", BODY)
    with pytest.raises(HTTPException) as exc:
        idempotency.begin(session, tenant, "k1", {**BODY, "customer": "cus_999"})
    assert exc.value.status_code == 422


def test_missing_key_is_400(session, tenant):
    with pytest.raises(HTTPException) as exc:
        idempotency.begin(session, tenant, None, BODY)
    assert exc.value.status_code == 400
