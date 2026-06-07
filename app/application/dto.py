from uuid import UUID

from pydantic import BaseModel


class CreateOrderDTO(BaseModel):
    user_id: str
    quantity: int
    item_id: UUID
    idempotency_key: str
