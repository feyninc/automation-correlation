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


def test_concurrent_first_requests_one_claims_other_gets_409(engine, session, tenant):
    """Two requests with a new key at the same moment: one runs, the other gets 409 (not a 500)."""
    import threading

    from sqlalchemy.orm import Session

    for attempt in range(20):
        key, outcomes, barrier = f"race-{attempt}", [], threading.Barrier(2)

        def call():
            with Session(engine) as s:
                barrier.wait()
                try:
                    outcomes.append(idempotency.begin(s, tenant, key, BODY))
                except HTTPException as exc:
                    outcomes.append(exc.status_code)

        threads = [threading.Thread(target=call) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sorted(outcomes, key=str) == [409, None], outcomes


def test_same_key_in_two_tenants_is_independent(session, tenant):
    session.add(Tenant(id="ten_b", name="Tenant B", timezone="UTC"))
    session.commit()
    idempotency.begin(session, "ten_a", "order-1001", BODY)
    idempotency.complete(session, "ten_a", "order-1001", 201, {"id": "in_a"})
    assert idempotency.begin(session, "ten_b", "order-1001", BODY) is None
    idempotency.complete(session, "ten_b", "order-1001", 201, {"id": "in_b"})
    assert idempotency.begin(session, "ten_b", "order-1001", BODY).response_body == {"id": "in_b"}
