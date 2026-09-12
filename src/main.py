import json
import logging
import os
from logging import Logger

from adapters.secret_manager_adapter import SecretsManagerAdapter, SecretsManagerPort
from adapters.stripe_adapter import StripeAdapter
from adapters.stripe_adapter.port import StripePort
from adapters.wix_adapter import WixAdapter
from adapters.wix_adapter.models import WixOrder, WixOrderLineItem
from adapters.wix_adapter.port import WixPort
from adapters.xero_adapter import XeroAdapter
from adapters.xero_adapter.models import OAuthToken, XeroLineItem
from adapters.xero_adapter.port import XeroPort
from models import Result, XeroLambdaSecrets

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def sync(
    logger: Logger,
    wix: WixPort,
    stripe: StripePort,
    xero: XeroPort,
    stripe_contact_id: str,
    xero_account_id: str,
) -> Result:
    logger.info("Getting recent Xero bank transactions")
    xero_bank_transactions = xero.list_bank_transactions()

    logger.info("Getting recent Stripe charges")
    stripe_charges_to_sync = [
        charge
        for charge in stripe.get_charges()
        if charge.source not in [xbt.reference for xbt in xero_bank_transactions]
    ]

    logger.info(f"{len(stripe_charges_to_sync)} fees will be synced to Xero")
    for stripe_charge in stripe_charges_to_sync:
        logger.info(f"Syncing Stripe fee for charge {stripe_charge.source}")
        xero.create_bank_transaction(
            amount=f"{stripe_charge.fee / 100}",
            reference=stripe_charge.source,
            date=stripe_charge.created,
            contact_id=stripe_contact_id,
            description="Stripe Fee",
            account_code="506",
            account_id=xero_account_id,
        )

    logger.info("Getting recent Xero invoices")
    xero_invoices = xero.list_invoices()

    logger.info("Getting recent Wix orders")
    wix_orders_to_sync = [
        wix_order
        for wix_order in wix.list_orders()
        if _wix_order_to_xero_reference(wix_order)
        not in [xero_invoice.reference for xero_invoice in xero_invoices]
    ]

    logger.info(f"{len(wix_orders_to_sync)} orders will be synced to Xero")
    for wix_order in wix_orders_to_sync:
        logger.info(f"Syncing Wix order {wix_order.order_number} to Xero invoice")
        _sync_wix_order_to_xero_invoice(xero, wix_order)

    logger.info("Finished Xero Lambda function")
    return Result(
        synced_stripe_charges=[
            stripe_charge.source for stripe_charge in stripe_charges_to_sync
        ],
        synced_wix_orders=[wix_order.order_number for wix_order in wix_orders_to_sync],
    )


def _get_secrets(secrets_manager: SecretsManagerPort) -> XeroLambdaSecrets:
    if (lambda_secret_string := secrets_manager.get_secret("xero_lambda")) is None:
        raise RuntimeError("No secret data found in xero_lambda secret")
    else:
        return XeroLambdaSecrets.from_json_string(lambda_secret_string)


def _initialize_xero_client(
    secret: XeroLambdaSecrets, secret_manager: SecretsManagerAdapter
) -> XeroAdapter:
    _xero_oauth_token_secret_name = "xero_lambda_oauth_token"

    oauth_token = _get_xero_oauth_token(
        secret_manager=secret_manager, secret_name=_xero_oauth_token_secret_name
    )

    xero = XeroAdapter(
        client_id=secret.xero_client_id,
        client_secret=secret.xero_client_secret,
        oauth_token=oauth_token,
        tenant_id=secret.xero_tenant_id,
    )

    if oauth_token != xero.oauth_token:
        secret_manager.store_secret(
            secret_name=_xero_oauth_token_secret_name,
            value=json.dumps(xero.oauth_token.__dict__),
        )

    return xero


def _get_xero_oauth_token(
    secret_manager: SecretsManagerAdapter, secret_name: str
) -> OAuthToken:
    oauth_string = secret_manager.get_secret(secret_name)

    if oauth_string is not None:
        return OAuthToken(**json.loads(oauth_string))
    else:
        # Bootstrap token
        return OAuthToken(
            access_token=os.environ.get("XERO_BOOTSTRAP_ACCESS_TOKEN", ""),
            expires_in=1800,
            token_type="Bearer",
            refresh_token=os.environ.get("XERO_BOOTSTRAP_REFRESH_TOKEN", ""),
            scope=[
                "accounting.transactions",
                "accounting.contacts",
                "offline_access",
                "openid",
            ],
        )


def _sync_wix_order_to_xero_invoice(xero_adapter: XeroPort, wix_order: WixOrder):
    xero_contact = (
        contact
        if (contact := xero_adapter.get_contact(wix_order.buyer_email)) is not None
        else xero_adapter.create_contact(
            name=f"{wix_order.contact_firstname} {wix_order.contact_lastname}",
            email=wix_order.buyer_email,
        )
    )

    xero_adapter.create_invoice(
        contact_id=xero_contact.contact_id,
        date=wix_order.created_date,
        line_items=list(
            map(_wix_order_line_item_to_xero_line_item, wix_order.line_items)
        )
        + [_xero_line_item_from_wix_shipping(wix_order)],
        reference=_wix_order_to_xero_reference(wix_order),
    )


def _wix_order_to_xero_reference(order: WixOrder) -> str:
    return f"WIX_{order.order_number}"


def _wix_order_line_item_to_xero_line_item(
    wix_line_item: WixOrderLineItem,
) -> XeroLineItem:
    return XeroLineItem(
        unit_amount=wix_line_item.amount,
        discount_amount=wix_line_item.discount_amount,
        quantity=wix_line_item.quantity,
        item_code=wix_line_item.sku,
        description=wix_line_item.product_name,
        account_code="200",
    )


def _xero_line_item_from_wix_shipping(wix_order: WixOrder) -> XeroLineItem:
    return XeroLineItem(
        unit_amount=wix_order.shipping_info.amount,
        discount_amount=None,
        quantity=1,
        description=wix_order.shipping_info.title,
        item_code=wix_order.shipping_info.title,
        account_code="448",
    )


if __name__ == "__main__":
    logger = logging.getLogger("xero-sync")
    logger.info("Starting Xero Lambda function")

    logger.info("Initialising Secrets Manager adapter")
    secrets_manager = SecretsManagerAdapter()

    logger.info("Getting secrets")
    secret = _get_secrets(secrets_manager=secrets_manager)

    logger.info("Initialising Wix adapter")
    wix = WixAdapter(api_key=secret.wix_api_token, site_id=secret.wix_site_id)

    logger.info("Initialising Xero adapter")
    xero = _initialize_xero_client(secret, secrets_manager)

    logger.info("Initialising Stripe adapter")
    stripe = StripeAdapter(api_key=secret.stripe_api_token)

    sync(
        logger=logger,
        wix=wix,
        stripe=stripe,
        xero=xero,
        stripe_contact_id=secret.xero_contact_id_stripe,
        xero_account_id=secret.xero_account_id,
    )
