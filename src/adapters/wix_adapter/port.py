from abc import ABC, abstractmethod

from .models import WixOrder


class WixPort(ABC):
    @abstractmethod
    def list_orders(self) -> list[WixOrder]:
        pass
