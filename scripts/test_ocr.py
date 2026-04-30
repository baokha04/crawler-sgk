import asyncio
import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.infrastructure.database import init_db, AsyncSessionLocal
from app.domains.books.ocr_service import OCRService

async def test_ocr():
    print("Initializing database...")
    await init_db()
    
    image_name = "book_1_page_10.jpg"
    print(f"Testing OCR for {image_name}...")
    
    async with AsyncSessionLocal() as db:
        ocr_service = OCRService(db)
        try:
            # We already have a record from the previous run, let's just fetch it or re-run
            record = await ocr_service.process_and_store(image_name)
            print(f"Status: {record.status}")
            if record.status == "completed":
                output_file = "test_ocr_result.md"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(record.result_markdown)
                print(f"Success! Result written to {output_file}")
            else:
                print(f"Error: {record.result_markdown}")
        except Exception as e:
            print(f"Failed with exception: {e}")

if __name__ == "__main__":
    asyncio.run(test_ocr())
