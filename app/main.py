from fastapi import FastAPI

from app.utils.create_container import create_container

container = create_container()

app = FastAPI()


@app.get("/")
async def main_page():
    return {"status": "ok"}
