import uuid

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import OrderDomain, OrderStatusEnum
from app.infrastructure.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_order(self, new_order):
        order = Order(
            user_id=new_order.user_id,
            quantity=new_order.quantity,
            item_id=new_order.item_id,
            idempotency_key=new_order.idempotency_key,
            status=OrderStatusEnum.NEW,
        )
        self._session.add(order)
        await self._session.flush()
        return self._construct(order)

    async def update_status(self, order_id: uuid.UUID, status: OrderStatusEnum) -> None:

        await self._session.execute(
            update(Order).where(Order.id == order_id).values(status=status)
        )

        await self._session.flush()

    async def check_idempotency(self, idempotency_key: str):
        """Проверка наличия ключа идемпотентности"""
        result = await self._session.execute(
            select(Order).where(Order.idempotency_key == idempotency_key)
        )
        order = result.scalar_one_or_none()
        if order is None:
            return None
        return self._construct(order)

    async def get_order_by_id(self, order_id: uuid.UUID):
        stmt = await self._session.execute(select(Order).where(Order.id == order_id))
        order = stmt.scalar_one_or_none()

        if order is None:
            return None
        return self._construct(order)

    @staticmethod
    def _construct(order: Order) -> OrderDomain:
        """из модели бд в модель domain"""
        return OrderDomain(
            id=order.id,
            user_id=order.user_id,
            quantity=order.quantity,
            item_id=order.item_id,
            idempotency_key=order.idempotency_key,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
