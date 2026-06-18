import logging

from app.application.dto import PaymentFromCallback
from app.domain.models import OrderStatusEnum, PaymentStatusEnum
from app.infrastructure.uow import UnitOfWork

logger = logging.getLogger(__name__)


class PaymentCallbackUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def __call__(self, payment_data: PaymentFromCallback):
        async with self._unit_of_work() as uow:
            order = await uow.orders.get_order_by_id(payment_data.order_id)

            if order is None:
                logger.warning(
                    "Заказ %s, полученный в callback, не найден", payment_data.order_id
                )
                return

            if order.status in (OrderStatusEnum.PAID, OrderStatusEnum.CANCELLED):
                logger.warning(
                    "Заказ %s, полученный в callback, уже обработан",
                    payment_data.order_id,
                )
                return

            new_status = (
                OrderStatusEnum.PAID
                if payment_data.status == PaymentStatusEnum.succeeded
                else OrderStatusEnum.CANCELLED
            )

            await uow.orders.update_status(order_id=order.id, status=new_status)

            await uow.commit()
