from datetime import date
from decimal import Decimal

from app.billing.proration import BillingPeriod, downgrade_adjustment

NOVEMBER = BillingPeriod(date(2026, 11, 1), date(2026, 12, 1))


def test_november_has_30_days():
    assert NOVEMBER.days == 30


def test_downgrade_mid_month():
    credit, charge = downgrade_adjustment(Decimal("499.00"), Decimal("199.00"), date(2026, 11, 18), NOVEMBER)
    assert credit == Decimal("199.60")
    assert charge == Decimal("79.60")
