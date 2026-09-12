from abc import ABC, abstractmethod
from datetime import datetime

from .models import XeroBankTransaction, XeroContact, XeroInvoice, XeroLineItem


class XeroPort(ABC):
    @abstractmethod
    def list_invoices(self) -> list[XeroInvoice]:
        pass

    @abstractmethod
    def create_invoice(
        self,
        contact_id: str,
        date: datetime,
        line_items: list[XeroLineItem],
        reference: str,
    ) -> None:
        pass

    @abstractmethod
    def list_bank_transactions(self) -> list[XeroBankTransaction]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def get_contact(self, email: str) -> XeroContact | None:
        pass

    @abstractmethod
    def create_contact(self, name: str, email: str) -> XeroContact:
        pass
