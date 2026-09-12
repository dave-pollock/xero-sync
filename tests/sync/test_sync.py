import logging
from datetime import UTC, datetime
from logging import Logger, NullHandler

import pytest
from pytest_bdd import given, scenarios, then, when
from stubs.stripe import StripeStub
from stubs.wix import WixStub
from stubs.xero import XeroStub

from adapters.wix_adapter.models import WixOrder, WixOrderLineItem, WixShippingInfo
from main import sync

scenarios("./test_sync.feature")


@pytest.fixture
def wix() -> WixStub:
    return WixStub()


@pytest.fixture
def stripe() -> StripeStub:
    return StripeStub()


@pytest.fixture
def xero() -> XeroStub:
    return XeroStub()


@pytest.fixture
def logger() -> Logger:
    logger = logging.getLogger(__name__)
    logger.addHandler(NullHandler())
    return logger


@given("wix order with line items:", target_fixture="wix_orders")
def _(datatable: list[list[str]], wix: WixStub) -> None:
    wix.add_order(
        order=WixOrder(
            order_number=len(wix.list_orders()) + 1,
            line_items=[
                WixOrderLineItem(
                    amount=float(r[0]),
                    discount_amount=float(r[1]),
                    quantity=int(r[2]),
                    sku=r[3],
                    product_name=r[4],
                )
                for r in datatable[1:]
            ],
            buyer_email="test@test.com",
            contact_firstname="testfirst",
            contact_lastname="testlast",
            created_date=datetime.now(tz=UTC),
            shipping_info=WixShippingInfo(title="test shipment", amount=1.50),
        )
    )


@when("sync runs")
def _(logger: Logger, wix: WixStub, stripe: StripeStub, xero: XeroStub) -> None:
    sync(
        logger=logger,
        wix=wix,
        stripe=stripe,
        xero=xero,
        stripe_contact_id="test",
        xero_account_id="test-1",
    )


@then("the wix orders should exist in xero")
def _(wix: WixStub, xero: XeroStub) -> None:
    assert len(wix.list_orders()) == len(xero.list_invoices())
