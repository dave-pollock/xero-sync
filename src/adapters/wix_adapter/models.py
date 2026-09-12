from dataclasses import dataclass
from datetime import datetime
from typing import Self

from .api_models import Order, OrderLineItem


@dataclass
class WixOrderLineItem:
    amount: float | None
    discount_amount: float | None
    quantity: int
    sku: str
    product_name: str

    @classmethod
    def from_wix_order_line_item(cls, li: OrderLineItem) -> Self:
        return cls(
            amount=li.price_before_discounts.amount,
            discount_amount=(li.price_before_discounts.amount - li.price.amount),
            quantity=li.quantity,
            product_name=li.product_name.original,
            sku=li.physical_properties.sku,
        )


@dataclass
class WixShippingInfo:
    title: str
    amount: float


@dataclass
class WixOrder:
    order_number: int
    line_items: list[WixOrderLineItem]
    buyer_email: str
    contact_firstname: str
    contact_lastname: str
    created_date: datetime
    shipping_info: WixShippingInfo

    @classmethod
    def from_wix_order(cls, order: Order) -> Self:
        return cls(
            order_number=order.number,
            line_items=[
                WixOrderLineItem.from_wix_order_line_item(li) for li in order.line_items
            ],
            buyer_email=order.buyer_info.email,
            contact_firstname=order.billing_info.contact_details.first_name,
            contact_lastname=order.billing_info.contact_details.last_name,
            created_date=datetime.fromisoformat(order.created_date),
            shipping_info=WixShippingInfo(
                amount=order.shipping_info.cost.price.amount,
                title=order.shipping_info.title,
            ),
        )
