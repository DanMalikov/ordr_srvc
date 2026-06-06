from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.infrastructure.uow import UnitOfWork


class InfrastructureContainer(DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton[AsyncEngine](
        create_async_engine,
        config.get_db_string,
        echo=False,
        pool_pre_ping=True,
    )
    session_factory = providers.Singleton(
        async_sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    unit_of_work = providers.Factory(UnitOfWork, session_factory)
