import uuid
from datetime import datetime
from uuid import UUID

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from app.application.dto import CreateOrderDTO, PaymentFromCallback
from app.application.exceptions import ItemOutOfStock, OrderNotFound
from app.application.use_cases.create_order_use_case import CreateOrderUseCase
from app.application.use_cases.get_order_use_case import GetOrderUseCase
from app.container import AppContainer
from app.domain.exceptions import CompareQuantityError
from app.domain.models import OrderStatusEnum
from app.infrastructure.exceptions import CatalogRequestError, ItemNotFound

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
    updated_at: datetime


class AcceptPaymentCallback(PaymentFromCallback):
    pass


@order_router.post(
    "", response_model=ResponseOrderDTO, status_code=status.HTTP_201_CREATED
)
@inject
async def create_order(
    order_data: RequestCreateOrderDTO,
    create_order_use_case: CreateOrderUseCase = Depends(
        Provide[AppContainer.application.create_order_use_case]
    ),
):
    try:
        result = await create_order_use_case(order_data)
    except CatalogRequestError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)
        ) from exc
    except ItemNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except CompareQuantityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except ItemOutOfStock as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    return result


@order_router.get(
    "/{order_id}", response_model=ResponseOrderDTO, status_code=status.HTTP_200_OK
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
    except OrderNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    return order


@order_router.post("/payment_callback", status_code=status.HTTP_200_OK)
@inject
async def get_payment_by_callback(
    callback_data: AcceptPaymentCallback,
    payment_callback_use_case=Depends(
        Provide[AppContainer.application.payment_callback_use_case]
    ),
):

    await payment_callback_use_case(callback_data)

    return Response(status_code=status.HTTP_200_OK)
