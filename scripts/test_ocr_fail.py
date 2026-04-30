import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.future import select
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.models import OCRFail, ProcessMarkdown
from app.domains.books.ocr_service import OCRService

async def test_ocr_fail():
    async with AsyncSessionLocal() as db:
        image_name = "non_existent_image.jpg"
        print(f"Testing OCR failure recording for: {image_name}")

        ocr_service = OCRService(db)
        
        try:
            # This should fail because the file doesn't exist
            await ocr_service.process_and_store(image_name)
        except Exception as e:
            print(f"Caught expected error: {e}")

        # Verify failure recorded in OCRFail table
        result = await db.execute(
            select(OCRFail).where(OCRFail.image_name == image_name).order_by(OCRFail.created_at.desc())
        )
        fail_record = result.scalars().first()
        
        if fail_record:
            print(f"SUCCESS: Failure recorded in OCRFail table. ID: {fail_record.id}, Error: {fail_record.error_message}")
        else:
            print("FAILURE: No record found in OCRFail table.")

if __name__ == "__main__":
    asyncio.run(test_ocr_fail())
