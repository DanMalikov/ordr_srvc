from contextlib import asynccontextmanager


class UnitOfWork:
    def __init__(self): ...

    @asynccontextmanager
    async def __call__(self): ...


class _UnitOfWorkImplementation:
    def __init__(self): ...
