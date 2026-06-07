import uuid
from datetime import datetime
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.application.dto import CreateOrderDTO
from app.application.use_cases.create_order_use_case import CreateOrderUseCase
from app.application.use_cases.get_order_use_case import GetOrderUseCase
from app.container import AppContainer
from app.domain.models import OrderStatusEnum

order_router = APIRouter(prefix="/api/orders", tags=["orders"])


class RequestCreateOrderDTO(CreateOrderDTO):
    pass


class ResponseOrderDTO(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: UUID
    status: OrderStatusEnum
    created_at: datetime
    update_at: datetime


@order_router.post(
    "/", response_model=ResponseOrderDTO, status_code=status.HTTP_201_CREATED
)
@inject
async def create_order(
    order_data,
    create_order_use_case: CreateOrderUseCase = Depends(
        Provide[AppContainer.application.create_order_use_case]
    ),
):
    try:
        result = await create_order_use_case(order_data)
    except:
        raise
    return result


@order_router.get(
    "/{order_id}/", response_model=ResponseOrderDTO, status_code=status.HTTP_200_OK
)
@inject
async def get_order(
    order_id: uuid.UUID,
    get_order_use_case: GetOrderUseCase = Depends(
        Provide[AppContainer.application.get_order_use_case]
    ),
):
    try:
        order = await get_order_use_case(order_id)
    except:
        raise

    return order
