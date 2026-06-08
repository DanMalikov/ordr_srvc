import uuid
from datetime import datetime
from decimal import Decimal

import httpx
from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: uuid.UUID
    name: str
    price: Decimal
    available_qty: int
    created_at: datetime


class CatalogClient:
    def __init__(self, http_client: httpx.AsyncClient):
        self._client = http_client

    async def get_item(self, item_id: uuid.UUID) -> ItemResponse:
        try:
            response = await self._client.get(url=f"/api/catalog/items/{item_id}")
        except Exception:
            raise

        return ItemResponse.model_validate(response.json())
