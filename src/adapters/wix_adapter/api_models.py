from dataclasses import dataclass
from typing import Self

from dataclass_wizard import JSONWizard
from dataclass_wizard.enums import KeyCase


@dataclass
class TranslatableName:
    original: str


@dataclass
class PhysicalProperties:
    sku: str


@dataclass
class Amount:
    amount: float


@dataclass
class OrderLineItem:
    product_name: TranslatableName
    quantity: int
    physical_properties: PhysicalProperties
    price: Amount
    price_before_discounts: Amount


@dataclass
class ShippingCost:
    price: Amount
    total_price_before_tax: Amount
    total_price_after_tax: Amount
    discount: Amount | None = None


@dataclass
class ShippingInfo:
    title: str
    cost: ShippingCost


@dataclass
class ContactDetails:
    first_name: str
    last_name: str


@dataclass
class BillingInfo:
    contact_details: ContactDetails


@dataclass
class BuyerInfo:
    email: str


@dataclass
class Order(JSONWizard, load_case=KeyCase.CAMEL):  # pyright: ignore[reportGeneralTypeIssues, reportCallIssue]
    number: int
    created_date: str
    line_items: list[OrderLineItem]
    buyer_info: BuyerInfo
    shipping_info: ShippingInfo
    billing_info: BillingInfo

    @classmethod
    def from_json_list(cls, json_list: str) -> list[Self]:
        result = cls.from_json(json_list)  # type: ignore
        return result if isinstance(result, list) else [result]
