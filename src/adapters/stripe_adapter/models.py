from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Self

from stripe import BalanceTransaction


@dataclass
class StripeBalanceTransaction:
    transaction_id: str
    source: str
    fee: int
    created: datetime

    @classmethod
    def from_stripe_balance_transaction(cls, stripe_bt: BalanceTransaction) -> Self:
        return cls(
            transaction_id=stripe_bt["id"],
            source=stripe_bt["source"],
            fee=stripe_bt["fee"],
            created=datetime.fromtimestamp(stripe_bt["created"], tz=UTC),
        )
