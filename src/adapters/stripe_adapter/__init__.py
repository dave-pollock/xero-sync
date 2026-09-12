from datetime import UTC, datetime, timedelta

from stripe import StripeClient
from stripe.params._balance_transaction_list_params import (
    BalanceTransactionListParams,
    BalanceTransactionListParamsCreated,
)

from .models import StripeBalanceTransaction
from .port import StripePort


class StripeAdapter(StripePort):
    _client: StripeClient

    def __init__(self, api_key: str):
        self._client = StripeClient(api_key=api_key)

    def get_charges(self) -> list[StripeBalanceTransaction]:
        return [
            StripeBalanceTransaction.from_stripe_balance_transaction(bt)
            for bt in self._client.v1.balance_transactions.list(
                BalanceTransactionListParams(
                    created=BalanceTransactionListParamsCreated(
                        gt=int((datetime.now(tz=UTC) - timedelta(days=30)).timestamp())
                    ),
                    type="charge",
                )
            ).data
        ]
