"""Mid-period plan changes (INV-2287)."""
from dataclasses import dataclass
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


@dataclass(frozen=True)
class BillingPeriod:
    start: date  # first day of the period
    end: date  # first day of the next period (exclusive)

    @property
    def days(self) -> int:
        return (self.end - self.start).days


def prorate(amount: Decimal, days: int, period: BillingPeriod) -> Decimal:
    return (amount * days / period.days).quantize(CENT, rounding=ROUND_HALF_UP)


def downgrade_adjustment(
    old_price: Decimal, new_price: Decimal, change_date: date, period: BillingPeriod
) -> tuple[Decimal, Decimal]:
    """Credit for the old plan and charge for the new plan for the rest of the period."""
    # the customer was on the old plan for the change date itself
    remaining = (period.end - change_date).days - 1
    return prorate(old_price, remaining, period), prorate(new_price, remaining, period)
