from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database import get_db
from app.domains.books.book_service import BookService
from app.domains.books.crawler import SGKCrawler
from pydantic import BaseModel

router = APIRouter()

class CrawlRequest(BaseModel):
    url: str

@router.post("/crawl")
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    book_service = BookService(db)
    crawler = SGKCrawler(book_service)
    
    # Run crawl in background to avoid timeout
    background_tasks.add_task(crawler.crawl, request.url)
    
    return {"message": "Crawl started in background", "url": request.url}
