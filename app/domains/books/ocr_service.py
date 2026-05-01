import os
import asyncio
import google.generativeai as genai
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domains.config.service import ConfigService
from app.core.config import settings
from app.infrastructure.models import ProcessMarkdown, BookPage, OCRFail, OCRRateLimit
from datetime import datetime
import logging
import base64
import httpx
import json

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.config_service = ConfigService(db)
        self.provider = None
        self.model_name = None
        self.api_key = None
        self.gemini_model = None # For Google provider

    async def _ensure_configured(self, provider: str = None, model: str = None):
        # Load provider from config if not provided
        if not provider:
            provider = await self.config_service.get_active_config("ai_provider")
        if not provider:
            provider = settings.DEFAULT_AI_PROVIDER
        
        self.provider = provider

        if provider == "google":
            api_key = await self.config_service.get_active_config("google_api_key")
            if not api_key:
                api_key = settings.GOOGLE_API_KEY
            
            if not model:
                model = await self.config_service.get_active_config("ai_model")
            if not model:
                model = settings.GEMINI_MODEL_NAME
            
            self.model_name = model
            self.api_key = api_key

            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_model = genai.GenerativeModel(model)
            else:
                logger.warning("GOOGLE_API_KEY not found. OCR will not work.")
                raise ValueError("Google API Key not configured.")
        
        elif provider == "openrouter":
            api_key = await self.config_service.get_active_config("openrouter_api_key")
            if not api_key:
                api_key = settings.OPENROUTER_API_KEY
            
            if not model:
                # For openrouter, we might still check 'ai_model' config key if it's set specifically for openrouter
                model = await self.config_service.get_active_config("ai_model")
            if not model:
                model = settings.OPENROUTER_MODEL_NAME
            
            self.model_name = model
            self.api_key = api_key
            
            if not api_key:
                logger.warning("OPENROUTER_API_KEY not found. OCR will not work.")
                raise ValueError("OpenRouter API Key not configured.")
        else:
            raise ValueError(f"Unsupported AI provider: {provider}")

    async def convert_image_to_markdown(self, image_path: str, provider: str = None, model: str = None) -> str:
        await self._ensure_configured(provider, model)
        
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found at {image_path}")

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
            if self.provider == "google":
                return await self._ocr_google(image_path, prompt)
            elif self.provider == "openrouter":
                return await self._ocr_openrouter(image_path, prompt)
        except Exception as e:
            logger.error(f"Error during {self.provider} OCR: {str(e)}")
            raise

    async def _ocr_google(self, image_path: str, prompt: str) -> str:
        if not self.gemini_model:
            raise ValueError("Gemini model not configured.")
        
        img = Image.open(image_path)
        response = self.gemini_model.generate_content([prompt, img])
        return response.text

    async def _ocr_openrouter(self, image_path: str, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("OpenRouter API key not configured.")

        base64_image = self._encode_image(image_path)
        mime_type = self._get_mime_type(image_path)

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                content=json.dumps({
                    "model": self.model_name,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                })
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")
            
            data = response.json()
            if "choices" not in data or len(data["choices"]) == 0:
                raise Exception(f"Invalid response from OpenRouter: {data}")
            
            return data["choices"][0]["message"]["content"]

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _get_mime_type(self, image_path: str) -> str:
        ext = os.path.splitext(image_path)[1].lower()
        if ext in ['.jpg', '.jpeg']:
            return 'image/jpeg'
        if ext == '.png':
            return 'image/png'
        if ext == '.webp':
            return 'image/webp'
        return 'image/jpeg' # Default

    async def process_and_store(self, image_name: str, provider: str = None, model: str = None) -> ProcessMarkdown:
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

        # Always try to link to BookPage if not linked
        await self._link_to_book_page(image_name, process_record.id)

        if process_record.status == "completed":
            return process_record

        try:
            image_path = os.path.join("download", image_name)
            markdown_content = await self.convert_image_to_markdown(image_path, provider, model)
            
            process_record.result_markdown = markdown_content
            process_record.status = "completed"
            
            # Link again after completion to be sure
            await self._link_to_book_page(image_name, process_record.id)
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Failed to process {image_name}: {error_msg}")
            process_record.status = "failed"
            process_record.result_markdown = error_msg
            
            # Store failure in OCRFail table
            fail_record = OCRFail(image_name=image_name, error_message=error_msg)
            self.db.add(fail_record)
            
            await self.db.commit()
            await self.db.refresh(process_record)
            raise # Re-raise to stop process_all
        
        await self.db.commit()
        await self.db.refresh(process_record)
        return process_record

    async def _link_to_book_page(self, image_name: str, process_id: int):
        # image_path in DB is "download/filename"
        image_path = f"download/{image_name}"
        result = await self.db.execute(
            select(BookPage).where(BookPage.image_path == image_path)
        )
        book_page = result.scalars().first()
        if book_page and book_page.process_markdown_id != process_id:
            book_page.process_markdown_id = process_id
            self.db.add(book_page)

    async def process_all_images(self, provider: str = None, model: str = None) -> dict:
        download_dir = "download"
        if not os.path.exists(download_dir):
            return {"status": "error", "message": "Download directory not found"}

        # Get all image files
        files = [f for f in os.listdir(download_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        processed_count = 0
        skipped_count = 0
        
        for file_name in files:
            # Check if already processed and linked
            result = await self.db.execute(
                select(ProcessMarkdown).where(ProcessMarkdown.image_name == file_name)
            )
            process_record = result.scalars().first()
            
            if process_record and process_record.status == "completed":
                # Check if linked to BookPage
                image_path = f"{download_dir}/{file_name}"
                page_result = await self.db.execute(
                    select(BookPage).where(BookPage.image_path == image_path)
                )
                book_page = page_result.scalars().first()
                if book_page and book_page.process_markdown_id == process_record.id:
                    skipped_count += 1
                    continue
            
            try:
                # Check rate limit before each processing
                await self._check_rate_limit()
                
                await self.process_and_store(file_name, provider, model)
                processed_count += 1
            except Exception as e:
                # Stop processing on error as requested
                return {
                    "status": "failed",
                    "message": f"Stopped due to error on {file_name}: {str(e)}",
                    "processed_count": processed_count,
                    "skipped_count": skipped_count
                }
        
        return {
            "status": "completed",
            "processed_count": processed_count,
            "skipped_count": skipped_count
        }

    async def _check_rate_limit(self):
        # Use SELECT ... FOR UPDATE to handle concurrency
        result = await self.db.execute(
            select(OCRRateLimit).where(OCRRateLimit.id == 1).with_for_update()
        )
        rate_limit = result.scalars().first()
        
        now = datetime.utcnow()
        if not rate_limit:
            rate_limit = OCRRateLimit(id=1, current_count=1, window_start=now)
            self.db.add(rate_limit)
            await self.db.commit()
            return

        window_duration = (now - rate_limit.window_start).total_seconds()
        
        if window_duration >= 60:
            # New window
            rate_limit.current_count = 1
            rate_limit.window_start = now
        else:
            if rate_limit.current_count < 15:
                # Still within limit
                rate_limit.current_count += 1
            else:
                # Limit reached, wait
                wait_time = 60 - window_duration + 1.0 # Add a small buffer
                logger.info(f"OCR rate limit reached (15/min). Waiting for {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
                # Reset after wait
                rate_limit.current_count = 1
                rate_limit.window_start = datetime.utcnow()
        
        self.db.add(rate_limit)
        await self.db.commit()
