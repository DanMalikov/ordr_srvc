from app.application.dto import CreateOrderDTO
from app.domain.models import OrderDomain
from app.infrastructure.http_reqs.http_catalog import CatalogClient
from app.infrastructure.uow import UnitOfWork


class CreateOrderUseCase:
    def __init__(self, unit_of_work: UnitOfWork, catalog_client: CatalogClient):
        self._unit_of_work = unit_of_work
        self._catalog_client = catalog_client

    async def __call__(self, new_order: CreateOrderDTO) -> OrderDomain:
        async with self._unit_of_work() as uow:
            check_idempotency = await uow.orders.check_idempotency(
                new_order.idempotency_key
            )

            if check_idempotency is not None:
                return check_idempotency

            catalog_item = await self._catalog_client.get_item(new_order.item_id)

            order = await uow.orders.create_order(new_order)

            order.validate_quantity(catalog_item.available_qty)

            await uow.commit()

            return order
