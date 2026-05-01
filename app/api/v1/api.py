from fastapi import APIRouter
from app.api.v1.endpoints import books, ocr, config

api_router = APIRouter()

api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(ocr.router, prefix="/ocr", tags=["ocr"])
api_router.include_router(config.router, prefix="/configs", tags=["configs"])

@api_router.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}
