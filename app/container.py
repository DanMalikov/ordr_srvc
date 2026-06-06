from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.application.container import ApplicationContainer
from app.infrastructure.container import InfrastructureContainer


class AppContainer(DeclarativeContainer):
    config = providers.Configuration()

    infrastructure = providers.Container(InfrastructureContainer, config=config)

    application = providers.Container(
        ApplicationContainer, infrastructure=infrastructure, config=config
    )
