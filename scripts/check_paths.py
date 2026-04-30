import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy.future import select
from app.infrastructure.database import AsyncSessionLocal
from app.infrastructure.models import BookPage

async def check():
    async with AsyncSessionLocal() as db:
        res = await db.execute(select(BookPage).limit(5))
        for r in res.scalars():
            print(f"ID: {r.id}, Path: {r.image_path}")

if __name__ == "__main__":
    asyncio.run(check())
