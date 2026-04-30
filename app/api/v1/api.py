from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.endpoints import books
api_router.include_router(books.router, prefix="/books", tags=["books"])

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
