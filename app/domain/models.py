from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel

from app.domain.exceptions import CompareQuantityError


class OrderStatusEnum(StrEnum):
    NEW = "NEW"
    "заказ создан"

    PAID = "PAID"
    "латеж успешен"

    SHIPPED = "SHIPPED"
    "заказ отправлен"

    CANCELLED = "CANCELLED"
    "заказ отменен"


class PaymentStatusEnum(StrEnum):
    succeeded = "succeeded"
    failed = "failed"


class OrderDomain(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: str
    status: OrderStatusEnum
    created_at: datetime
    updated_at: datetime

    def validate_quantity(self, actual_quantity):
        if self.quantity > actual_quantity:
            raise CompareQuantityError(
                "Для бронирования указано неверное количество товара"
            )
