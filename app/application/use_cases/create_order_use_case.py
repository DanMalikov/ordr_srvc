from app.infrastructure.uow import UnitOfWork


class CreateOrderUseCase:
    def __init__(self, unit_of_work: UnitOfWork):
        self._unit_of_work = unit_of_work

    async def __call__(self):
        async with self._unit_of_work as uow:
            uow.commit()
