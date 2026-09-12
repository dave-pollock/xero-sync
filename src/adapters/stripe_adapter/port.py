from abc import ABC, abstractmethod

from .models import StripeBalanceTransaction


class StripePort(ABC):
    @abstractmethod
    def get_charges(self) -> list[StripeBalanceTransaction]:
        pass
