import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.future import select
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.models import BookPage, ProcessMarkdown
from app.domains.books.ocr_service import OCRService

async def test_linking():
    async with AsyncSessionLocal() as db:
        # 1. Create a dummy BookPage if none exists
        result = await db.execute(select(BookPage).limit(1))
        book_page = result.scalars().first()
        
        if not book_page:
            print("No BookPage found in DB. Please run a crawl first.")
            return

        image_name = os.path.basename(book_page.image_path)
        print(f"Testing linking for image: {image_name}")

        ocr_service = OCRService(db)
        
        # 2. Mock a ProcessMarkdown record
        pm_result = await db.execute(
            select(ProcessMarkdown).where(ProcessMarkdown.image_name == image_name)
        )
        pm = pm_result.scalars().first()
        if not pm:
            pm = ProcessMarkdown(image_name=image_name, status="completed", result_markdown="Test content")
            db.add(pm)
            await db.commit()
            await db.refresh(pm)
            print(f"Created mock ProcessMarkdown with ID: {pm.id}")
        else:
            print(f"Found existing ProcessMarkdown with ID: {pm.id}")

        # 3. Call the linking method
        await ocr_service._link_to_book_page(image_name, pm.id)
        await db.commit()
        
        # 4. Verify linking
        await db.refresh(book_page)
        if book_page.process_markdown_id == pm.id:
            print(f"SUCCESS: BookPage {book_page.id} linked to ProcessMarkdown {pm.id}")
        else:
            print(f"FAILURE: BookPage {book_page.id} NOT linked. Expected {pm.id}, got {book_page.process_markdown_id}")

if __name__ == "__main__":
    asyncio.run(test_linking())
