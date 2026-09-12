from datetime import UTC, datetime, timedelta

import requests

from .api_models import Order
from .models import WixOrder
from .port import WixPort


class WixAdapter(WixPort):
    _headers: dict[str, str]
    _base_url = "https://www.wixapis.com/ecom/v1"

    def __init__(self, api_key: str, site_id: str):
        self._headers = {"Authorization": api_key, "wix-site-id": site_id}

    def list_orders(self) -> list[WixOrder]:
        response = requests.post(
            url=f"{self._base_url}/orders/search",
            headers=self._headers,
            json={
                "search": {
                    "filter": {
                        "createdDate": {
                            "$gte": (datetime.now(tz=UTC) - timedelta(days=30))
                            .replace(tzinfo=None)
                            .isoformat()
                        }
                    }
                }
            },
        )
        response.raise_for_status()

        return [
            WixOrder.from_wix_order(Order.from_dict(o))
            for o in response.json().get("orders", [])
        ]
