import os
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infrastructure.models import Book, BookPage
from typing import Optional

class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.download_dir = "download"
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    async def get_or_create_book(self, title: str, url: str, total_pages: int) -> Book:
        query = select(Book).where(Book.url == url)
        result = await self.db.execute(query)
        book = result.scalar_one_or_none()

        if not book:
            book = Book(title=title, url=url, total_pages=total_pages)
            self.db.add(book)
            await self.db.commit()
            await self.db.refresh(book)
        return book

    async def add_page(self, book_id: int, page_number: int, image_url: str) -> BookPage:
        # Check if page already exists
        query = select(BookPage).where(BookPage.book_id == book_id, BookPage.page_number == page_number)
        result = await self.db.execute(query)
        page = result.scalar_one_or_none()

        if not page:
            page = BookPage(book_id=book_id, page_number=page_number, image_url=image_url)
            self.db.add(page)
            await self.db.commit()
            await self.db.refresh(page)
        
        # Download image
        image_path = await self.download_image(image_url, book_id, page_number)
        if image_path:
            page.image_path = image_path
            await self.db.commit()
        
        return page

    async def download_image(self, url: str, book_id: int, page_number: int) -> Optional[str]:
        try:
            if url.startswith("data:image"):
                # Handle base64
                header, data = url.split(",", 1)
                ext = header.split(";")[0].split("/")[1]
                import base64
                img_data = base64.b64decode(data)
                filename = f"book_{book_id}_page_{page_number}.{ext}"
                filepath = os.path.join(self.download_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                return filepath
            else:
                # Handle URL
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    if response.status_code == 200:
                        ext = url.split(".")[-1] if "." in url else "jpg"
                        filename = f"book_{book_id}_page_{page_number}.{ext}"
                        filepath = os.path.join(self.download_dir, filename)
                        with open(filepath, "wb") as f:
                            f.write(response.content)
                        return filepath
        except Exception as e:
            print(f"Error downloading image: {e}")
        return None
