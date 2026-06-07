from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.application.use_cases.create_order_use_case import CreateOrderUseCase
from app.application.use_cases.get_order_use_case import GetOrderUseCase


class ApplicationContainer(DeclarativeContainer):
    infrastructure = providers.DependenciesContainer()
    config = providers.Configuration()

    create_order_use_case = providers.Factory(
        CreateOrderUseCase, unit_of_work=infrastructure.unit_of_work
    )

    get_order_use_case = providers.Factory(
        GetOrderUseCase, unit_of_work=infrastructure.unit_of_work
    )
