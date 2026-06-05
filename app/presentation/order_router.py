from fastapi import APIRouter

order_router = APIRouter(prefix="/v1/orders", tags=["orders"])


@order_router.post("/")
async def blob():
    return
