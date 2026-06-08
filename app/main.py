from contextlib import asynccontextmanager

from fastapi import FastAPI

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


@app.get("/")
async def main_page():
    return {"status": "ok"}
