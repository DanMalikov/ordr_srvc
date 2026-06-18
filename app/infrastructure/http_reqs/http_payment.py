import logging
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import httpx
from pydantic import BaseModel

from app.application.dto import PaymentRequest
from app.application.exceptions import PaymentClientNotAvailable

logger = logging.getLogger(__name__)


class PaymentResponse(BaseModel):
    id: UUID
    user_id: UUID
    order_id: UUID
    amount: Decimal
    status: str
    idempotency_key: str
    created_at: datetime


class PaymentClient:
    def __init__(self, http_client, api_key):
        self.http_client = http_client
        self.api_key = api_key

    async def get_payment(self, payload: PaymentRequest):
        try:
            logger.info(
                "Отправка запроса в сервис Payment.Id заказа=%s", payload.order_id
            )

            response = await self.http_client.post(
                url="/api/payments",
                headers={"X-API-Key": self.api_key},
                json=payload.model_dump(mode="json"),
            )
        except httpx.RequestError as exc:
            raise PaymentClientNotAvailable(
                f"Ошибка подключения к сервису Payment. {exc}"
            ) from exc

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise PaymentClientNotAvailable(
                f"Ошибка в ответе сервиса Payment. {exc}"
            ) from exc

        return PaymentResponse.model_validate(response.json())
