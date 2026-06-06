from app.config import settings
from app.container import AppContainer


def create_container():
    container = AppContainer()
    container.config.from_keys(settings.model_dump())
    container.wire(packages=["app.presentation"])

    return container
