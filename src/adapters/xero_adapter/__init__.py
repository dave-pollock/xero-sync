from copy import deepcopy
from datetime import UTC, datetime, timedelta
from typing import Any

from xero_python.accounting import AccountingApi  # type:ignore
from xero_python.accounting.models import (  # type: ignore
    Account,
    BankTransaction,
    BankTransactions,
    Contact,
    Contacts,
    Invoice,
    Invoices,
    LineAmountTypes,
    LineItem,
)
from xero_python.api_client import ApiClient  # type: ignore
from xero_python.api_client.configuration import Configuration  # type: ignore
from xero_python.api_client.oauth2 import OAuth2Token  # type: ignore

from .models import (
    OAuthToken,
    XeroBankTransaction,
    XeroContact,
    XeroInvoice,
    XeroLineItem,
)
from .port import XeroPort


class XeroAdapter(XeroPort):
    _api_client: ApiClient
    _accounting: AccountingApi
    _tenant_id: str
    oauth_token: OAuthToken

    # To get the refresh token:
    # 1. Visit https://login.xero.com/identity/connect/authorize?response_type=code&client_id=*****&redirect_uri=*****&scope=accounting.transactions accounting.contacts offline_access
    # 2. Extract the code from the url you are redirected to after authorizing
    # 3. Run this replacing the code with one from above: (Invoke-WebRequest -uri "https://identity.xero.com/connect/token" -Method POST -Headers @{"Authorization"="Basic *****"} -ContentType "application/x-www-form-urlencoded" -Body "grant_type=authorization_code&code=*****&redirect_uri=*****").Content
    # 4. Extract the refresh token from the response
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        oauth_token: OAuthToken,
        tenant_id: str,
    ):
        self._api_client = ApiClient(
            Configuration(
                oauth2_token=OAuth2Token(
                    client_id=client_id,
                    client_secret=client_secret,
                ),
            ),
            pool_threads=1,
            oauth2_token_getter=self._get_oauth_token,
            oauth2_token_saver=self._store_oauth_token,
        )
        self.oauth_token = deepcopy(oauth_token)
        self._tenant_id = deepcopy(tenant_id)
        self._accounting = AccountingApi(api_client=self._api_client)
        self._api_client.refresh_oauth2_token()

    def _get_oauth_token(self) -> dict[str, Any]:
        return self.oauth_token.__dict__

    def _store_oauth_token(self, oauth_token: dict[str, Any]) -> None:
        self.oauth_token = OAuthToken(**oauth_token)

    def list_invoices(self) -> list[XeroInvoice]:
        return [
            XeroInvoice.from_invoice(i)  # type: ignore
            for i in self._accounting.get_invoices(  # type: ignore
                xero_tenant_id=self._tenant_id,
                if_modified_since=(datetime.now(tz=UTC) - timedelta(days=30)),  # type: ignore
                statuses=["DRAFT", "SUBMITTED", "AUTHORISED", "PAID"],  # type: ignore
            ).invoices  # type: ignore
        ]

    def create_invoice(
        self,
        contact_id: str,
        date: datetime,
        line_items: list[XeroLineItem],
        reference: str,
    ) -> None:
        self._accounting.create_invoices(  # type: ignore
            xero_tenant_id=self._tenant_id,
            invoices=Invoices(
                invoices=[
                    Invoice(
                        type="ACCREC",
                        contact=Contact(contact_id=contact_id),
                        date=date,
                        due_date=date + timedelta(days=7),
                        line_amount_types=LineAmountTypes.EXCLUSIVE,
                        line_items=self._to_line_items(line_items),
                        reference=reference,
                        status="AUTHORISED",
                    )
                ]
            ),
        )

    def list_bank_transactions(self) -> list[XeroBankTransaction]:
        return [
            XeroBankTransaction.from_bank_transaction(xbt)  # type: ignore
            for xbt in self._accounting.get_bank_transactions(  # type: ignore
                xero_tenant_id=self._tenant_id,
                if_modified_since=(datetime.now(tz=UTC) - timedelta(days=30)).strftime(
                    "%a, %d %b %Y %H:%M:%S UTC"
                ),  # type: ignore
                where='Status=="AUTHORISED"',  # type: ignore
            ).bank_transactions  # type: ignore
        ]

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
        self._accounting.create_bank_transactions(  # type: ignore
            xero_tenant_id=self._tenant_id,
            bank_transactions=BankTransactions(
                bank_transactions=[
                    BankTransaction(
                        type="SPEND",
                        contact=XeroContact(contact_id=contact_id),
                        date=date,
                        line_items=[
                            LineItem(
                                description=description,
                                unit_amount=amount,
                                account_code=account_code,
                            )
                        ],
                        reference=reference,
                        bank_account=Account(account_id=account_id),
                    )
                ]
            ),
        )

    def get_contact(self, email: str) -> XeroContact | None:
        return (
            XeroContact.from_contact(contacts[0])  # type: ignore
            if (
                contacts := self._accounting.get_contacts(  # type: ignore
                    xero_tenant_id=self._tenant_id,
                    summary_only=True,  # type: ignore
                    where=f'EmailAddress=="{email}"',  # type: ignore
                ).contacts  # type: ignore
            )
            else None
        )

    def create_contact(self, name: str, email: str) -> XeroContact:
        return XeroContact.from_contact(
            self._accounting.create_contacts(  # type: ignore
                xero_tenant_id=self._tenant_id,
                contacts=Contacts(contacts=[Contact(name=name, email_address=email)]),
            ).contacts[0]  # type: ignore
        )

    def _to_line_items(self, line_items: list[XeroLineItem]) -> list[LineItem]:
        return [
            LineItem(
                description=li.description,
                quantity=li.quantity,
                unit_amount=li.unit_amount,
                account_code=li.account_code,
                discount_amount=li.discount_amount,
                item_code=li.item_code,
            )
            for li in line_items
        ]
