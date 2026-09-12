from adapters.wix_adapter.models import WixOrder
from adapters.wix_adapter.port import WixPort


class WixStub(WixPort):
    _orders: dict[int, WixOrder]

    def __init__(self):
        self._orders = {}

    def list_orders(self) -> list[WixOrder]:
        return list(self._orders.values())

    def add_order(self, order: WixOrder) -> None:
        self._orders[order.order_number] = order
