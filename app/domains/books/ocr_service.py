import os
import google.generativeai as genai
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.config import settings
from app.infrastructure.models import ProcessMarkdown
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, db: AsyncSession):
        self.db = db
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)
        else:
            self.model = None
            logger.warning("GOOGLE_API_KEY not set. OCR will not work.")

    async def convert_image_to_markdown(self, image_path: str) -> str:
        if not self.model:
            raise ValueError("Gemini model not configured. Check GOOGLE_API_KEY.")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

        # Load image
        img = Image.open(image_path)

        prompt = """
Please perform high-fidelity OCR on this image and convert the content into structured Markdown format. The content contains Vietnamese, so pay close attention to diacritics and special characters to ensure 100% accuracy in spelling.
Requirements:
Maintain the original hierarchy of headings (using #, ##, ###).
Reconstruct all tables accurately using Markdown table syntax.
Preserve text styles such as bold, italics, and lists (bulleted or numbered).
If there are any mathematical formulas or technical symbols, render them in LaTeX.
Output the final result in clean Markdown code. Do not summarize or omit any information.
        """.strip()

        try:
            response = self.model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Error during Gemini OCR: {str(e)}")
            raise

    async def process_and_store(self, image_name: str) -> ProcessMarkdown:
        # Check if already exists
        result = await self.db.execute(
            select(ProcessMarkdown).where(ProcessMarkdown.image_name == image_name)
        )
        process_record = result.scalars().first()

        if not process_record:
            process_record = ProcessMarkdown(image_name=image_name, status="pending")
            self.db.add(process_record)
            await self.db.commit()
            await self.db.refresh(process_record)

        if process_record.status == "completed":
            return process_record

        try:
            image_path = os.path.join("download", image_name)
            markdown_content = await self.convert_image_to_markdown(image_path)
            
            process_record.result_markdown = markdown_content
            process_record.status = "completed"
        except Exception as e:
            logger.error(f"Failed to process {image_name}: {str(e)}")
            process_record.status = "failed"
            process_record.result_markdown = str(e)
        
        await self.db.commit()
        await self.db.refresh(process_record)
        return process_record
