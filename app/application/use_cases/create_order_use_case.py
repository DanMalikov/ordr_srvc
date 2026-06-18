import logging

from app.application.dto import CreateOrderDTO, PaymentRequest
from app.application.exceptions import ItemOutOfStock, PaymentClientNotAvailable
from app.domain.models import OrderDomain, OrderStatusEnum
from app.infrastructure.http_reqs.http_catalog import CatalogClient
from app.infrastructure.http_reqs.http_payment import PaymentClient
from app.infrastructure.uow import UnitOfWork

logger = logging.getLogger(__name__)


class CreateOrderUseCase:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        catalog_client: CatalogClient,
        payment_client: PaymentClient,
        callback_url: str,
    ):
        self._unit_of_work = unit_of_work
        self._catalog_client = catalog_client
        self._payment_client = payment_client
        self._callback_url = callback_url

    async def __call__(self, new_order: CreateOrderDTO) -> OrderDomain:
        async with self._unit_of_work() as uow:
            logger.info("Проверка ключа идемпотентности при создании заказа")

            check_idempotency = await uow.orders.check_idempotency(
                new_order.idempotency_key
            )

            if check_idempotency is not None:
                logger.warning(
                    "Ключ идемпотентности %s уже есть", new_order.idempotency_key
                )

                return check_idempotency

            catalog_item = await self._catalog_client.get_item(new_order.item_id)

            if catalog_item.available_qty == 0:
                raise ItemOutOfStock(
                    f"Предмет {catalog_item.name} с id {catalog_item.id} закончился"
                )

            order = await uow.orders.create_order(new_order)

            logger.info("Создан заказ %s", order.id)

            order.validate_quantity(catalog_item.available_qty)

            try:
                await self._payment_client.get_payment(
                    PaymentRequest(
                        order_id=order.id,
                        amount=catalog_item.price * order.quantity,
                        callback_url=self._callback_url,
                        idempotency_key=order.idempotency_key,
                    )
                )
            except PaymentClientNotAvailable:
                await uow.order.update_status(
                    order_id=order.id, status=OrderStatusEnum.CANCELLED
                )
                await uow.commit()

            await uow.commit()

            return order
