from app.domain.models import OrderDomain
from app.infrastructure.uow import UnitOfWork


class GetOrderUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def __call__(self, order_id) -> OrderDomain:
        async with self._unit_of_work as uow:
            order = await uow.orders.get_order_by_id(order_id=order_id)

            return order
