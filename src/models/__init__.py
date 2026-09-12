from dataclasses import dataclass
from typing import Self

from dataclass_wizard import JSONWizard


@dataclass
class XeroLambdaSecrets(JSONWizard):
    xero_account_id: str
    xero_client_id: str
    xero_client_secret: str
    xero_tenant_id: str
    xero_contact_id_stripe: str
    stripe_api_token: str
    wix_api_token: str
    wix_site_id: str

    @classmethod
    def from_json_string(cls, json_string: str) -> Self:
        return cls.from_json(json_string)  # type: ignore


@dataclass
class Result(JSONWizard):
    synced_stripe_charges: list[str]
    synced_wix_orders: list[int]
