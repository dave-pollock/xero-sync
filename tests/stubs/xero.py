from datetime import datetime
from uuid import uuid4

from adapters.xero_adapter.models import (
    XeroBankTransaction,
    XeroContact,
    XeroInvoice,
    XeroLineItem,
)
from adapters.xero_adapter.port import XeroPort


class XeroStub(XeroPort):
    _contacts: dict[str, XeroContact]
    _invoices: dict[str, XeroInvoice]
    _transactions: dict[str, XeroBankTransaction]

    def __init__(self):
        self._invoices = {}
        self._transactions = {}
        self._contacts = {}

    def list_invoices(self) -> list[XeroInvoice]:
        return list(self._invoices.values())

    def create_invoice(
        self,
        contact_id: str,
        date: datetime,
        line_items: list[XeroLineItem],
        reference: str,
    ) -> None:
        invoice_id = str(uuid4())
        self._invoices[invoice_id] = XeroInvoice(
            invoice_id=invoice_id,
            reference=reference,
        )

    def list_bank_transactions(self) -> list[XeroBankTransaction]:
        return list(self._transactions.values())

    def create_bank_transaction(
        self,
        amount: str,
        reference: str,
        date: datetime,
        contact_id: str,
        description: str,
        account_code: str,
        account_id: str,
    ) -> None:
        transaction_id = str(uuid4())
        self._transactions[transaction_id] = XeroBankTransaction(
            bank_transaction_id=transaction_id, reference=reference
        )

    def get_contact(self, email: str) -> XeroContact | None:
        return self._contacts.get(email, None)

    def create_contact(self, name: str, email: str) -> XeroContact:
        contact = XeroContact(contact_id=email)
        self._contacts[email] = contact
        return contact
