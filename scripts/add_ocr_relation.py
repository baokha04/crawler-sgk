import asyncio
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import text
from app.infrastructure.database import engine

async def migrate():
    async with engine.begin() as conn:
        print("Starting migration...")
        
        # Add column to book_pages if not exists
        try:
            # Check if column exists first (PostgreSQL specific)
            result = await conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='book_pages' AND column_name='process_markdown_id'"
            ))
            if not result.fetchone():
                await conn.execute(text("ALTER TABLE book_pages ADD COLUMN process_markdown_id INTEGER REFERENCES process_markdown(id)"))
                print("Successfully added process_markdown_id column to book_pages table.")
            else:
                print("Column process_markdown_id already exists in book_pages table.")
        except Exception as e:
            print(f"Error adding column: {e}")

        # Create ocr_fail table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocr_fail (
                    id SERIAL PRIMARY KEY,
                    image_name VARCHAR,
                    error_message TEXT,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
                )
            """))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS ix_ocr_fail_image_name ON ocr_fail (image_name)"))
            print("Successfully created ocr_fail table and index.")
        except Exception as e:
            print(f"Error creating ocr_fail table: {e}")

        # Create ocr_rate_limit table
        try:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS ocr_rate_limit (
                    id SERIAL PRIMARY KEY,
                    current_count INTEGER DEFAULT 0,
                    window_start TIMESTAMP WITHOUT TIME ZONE DEFAULT now()
                )
            """))
            # Initialize the first row if it doesn't exist
            result = await conn.execute(text("SELECT id FROM ocr_rate_limit WHERE id = 1"))
            if not result.fetchone():
                await conn.execute(text("INSERT INTO ocr_rate_limit (id, current_count, window_start) VALUES (1, 0, now())"))
            print("Successfully created and initialized ocr_rate_limit table.")
        except Exception as e:
            print(f"Error creating ocr_rate_limit table: {e}")
        
        print("Migration completed.")

if __name__ == "__main__":
    asyncio.run(migrate())
