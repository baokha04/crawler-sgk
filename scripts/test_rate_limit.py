import asyncio
import os
import sys
from datetime import datetime, timedelta

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.future import select
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.models import OCRRateLimit
from app.domains.books.ocr_service import OCRService

async def test_rate_limit():
    async with AsyncSessionLocal() as db:
        print("Testing OCR rate limit logic...")
        
        # 1. Initialize or reset limit state to 14 requests
        result = await db.execute(select(OCRRateLimit).where(OCRRateLimit.id == 1))
        rate_limit = result.scalars().first()
        
        now = datetime.utcnow()
        if rate_limit:
            rate_limit.current_count = 14
            rate_limit.window_start = now
        else:
            rate_limit = OCRRateLimit(id=1, current_count=14, window_start=now)
            db.add(rate_limit)
        
        await db.commit()
        print("Set initial state to 14 requests in current window.")

        ocr_service = OCRService(db)
        
        # 2. First call (should be 15th, no wait)
        print("Calling _check_rate_limit (should be 15th)...")
        start_time = datetime.utcnow()
        await ocr_service._check_rate_limit()
        print(f"15th call completed in {(datetime.utcnow() - start_time).total_seconds():.2f}s")

        # 3. Second call (should be 16th, SHOULD WAIT)
        print("Calling _check_rate_limit (should be 16th - EXPECTED WAIT)...")
        start_time = datetime.utcnow()
        # This will wait ~60s unless we mock the window_start to be older
        # Let's mock window_start to be 55s ago so it only waits 5s
        await db.refresh(rate_limit)
        rate_limit.window_start = now - timedelta(seconds=55)
        await db.commit()
        
        await ocr_service._check_rate_limit()
        duration = (datetime.utcnow() - start_time).total_seconds()
        print(f"16th call completed in {duration:.2f}s")
        
        if duration >= 5:
            print("SUCCESS: Rate limit wait logic worked.")
        else:
            print(f"FAILURE: Expected wait of ~5s, but took {duration:.2f}s")

if __name__ == "__main__":
    asyncio.run(test_rate_limit())
