from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from app.domain.models import PaymentStatusEnum


class CreateOrderDTO(BaseModel):
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: str


class PaymentRequest(BaseModel):
    order_id: UUID
    amount: Decimal
    callback_url: str
    idempotency_key: str


class PaymentFromCallback(BaseModel):
    payment_id: UUID
    order_id: UUID
    status: PaymentStatusEnum
    amount: Decimal
    error_message: str | None = None
