from app.application.dto import CreateOrderDTO
from app.domain.models import OrderDomain
from app.infrastructure.uow import UnitOfWork


class CreateOrderUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def __call__(self, new_order: CreateOrderDTO) -> OrderDomain:
        async with self._unit_of_work() as uow:
            check_idempotency = await uow.orders.check_idempotency(
                new_order.idempotency_key
            )

            if check_idempotency is not None:
                return check_idempotency

            order = await uow.orders.create_order(new_order)

            uow.commit()

            return order
