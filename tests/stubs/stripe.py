from adapters.stripe_adapter.models import StripeBalanceTransaction
from adapters.stripe_adapter.port import StripePort


class StripeStub(StripePort):
    _charges: dict[str, StripeBalanceTransaction]

    def __init__(self):
        self._charges = {}

    def get_charges(self) -> list[StripeBalanceTransaction]:
        return list(self._charges.values())
