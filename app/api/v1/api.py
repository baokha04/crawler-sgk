from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.endpoints import orders, books
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(books.router, prefix="/books", tags=["books"])

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
