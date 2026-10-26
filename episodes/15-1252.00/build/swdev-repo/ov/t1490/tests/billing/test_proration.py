from datetime import date
from decimal import Decimal

import pytest

from app.billing.proration import BillingPeriod, downgrade_adjustment

NOVEMBER = BillingPeriod(date(2026, 11, 1), date(2026, 12, 1))


def test_november_has_30_days():
    assert NOVEMBER.days == 30


def test_downgrade_mid_month():
    credit, charge = downgrade_adjustment(Decimal("499.00"), Decimal("199.00"), date(2026, 11, 18), NOVEMBER)
    assert credit == Decimal("216.23")
    assert charge == Decimal("86.23")
    assert credit - charge == Decimal("130.00")


def test_downgrade_matches_prd_example():
    assert downgrade_adjustment(Decimal("300.00"), Decimal("100.00"), date(2026, 11, 21), NOVEMBER) == (
        Decimal("100.00"),
        Decimal("33.33"),
    )


def test_downgrade_on_first_and_last_day():
    assert downgrade_adjustment(Decimal("499.00"), Decimal("199.00"), date(2026, 11, 1), NOVEMBER) == (
        Decimal("499.00"),
        Decimal("199.00"),
    )
    assert downgrade_adjustment(Decimal("499.00"), Decimal("199.00"), date(2026, 11, 30), NOVEMBER) == (
        Decimal("16.63"),
        Decimal("6.63"),
    )


def test_downgrade_outside_period_is_rejected():
    with pytest.raises(ValueError):
        downgrade_adjustment(Decimal("499.00"), Decimal("199.00"), date(2026, 12, 1), NOVEMBER)
