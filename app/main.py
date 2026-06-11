from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.presentation.order_router import order_router
from app.utils.create_container import create_container

container = create_container()


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        yield
    finally:
        http_client = container.infrastructure.http_client()
        await http_client.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(order_router)


@app.get("/")
async def main_page():
    return {"status": "ok"}
