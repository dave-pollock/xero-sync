from dataclasses import dataclass
from typing import Self

from xero_python.accounting.models import (  # type: ignore
    BankTransaction,
    Contact,
    Invoice,
    LineItem,
)


@dataclass
class OAuthToken:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: str
    scope: list[str]
    id_token: str | None = None
    expires_at: float | None = None


@dataclass
class XeroBankTransaction:
    bank_transaction_id: str
    reference: str

    @classmethod
    def from_bank_transaction(cls, bank_transaction: BankTransaction) -> Self:
        return cls(
            bank_transaction_id=bank_transaction.bank_transaction_id,  # type: ignore
            reference=bank_transaction.reference,  # type: ignore
        )


@dataclass
class XeroContact:
    contact_id: str

    @classmethod
    def from_contact(cls, contact: Contact) -> Self:
        return cls(contact_id=contact.contact_id)  # type: ignore


@dataclass
class XeroInvoice:
    invoice_id: str
    reference: str

    @classmethod
    def from_invoice(cls, invoice: Invoice) -> Self:
        return cls(
            invoice_id=invoice.invoice_id,  # type: ignore
            reference=invoice.reference,  # type: ignore
        )


@dataclass
class XeroLineItem:
    unit_amount: float | None
    discount_amount: float | None
    quantity: float | None
    item_code: str
    description: str | None
    account_code: str

    @classmethod
    def from_xero_line_item(cls, li: LineItem) -> Self:
        return cls(
            unit_amount=li.unit_amount,  # type: ignore
            discount_amount=li.discount_amount,  # type: ignore
            quantity=li.quantity,  # type: ignore
            item_code=li.item_code,  # type: ignore
            description=li.description,  # type: ignore
            account_code=li.account_code,  # type: ignore
        )
