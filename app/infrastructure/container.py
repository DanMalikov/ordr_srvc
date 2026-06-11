from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.http_reqs.http_catalog import CatalogClient
from app.infrastructure.uow import UnitOfWork


class InfrastructureContainer(DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton[AsyncEngine](
        create_async_engine,
        config.get_postgres_connecion_string,
        echo=False,
        pool_pre_ping=True,
    )
    session_factory = providers.Singleton(
        async_sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    http_client = providers.Singleton(
        AsyncClient, base_url=config.capashino_base_url, timeout=5.0, trust_env=False
    )

    catalog_client = providers.Factory(
        CatalogClient, http_client=http_client, api_key=config.api_key
    )

    unit_of_work = providers.Factory(UnitOfWork, session_factory)
