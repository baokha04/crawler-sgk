from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.domains.books.ocr_service import OCRService
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter()

class OCRResponse(BaseModel):
    id: int
    image_name: str
    result_markdown: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/process/{image_name}", response_model=OCRResponse)
async def process_image_to_markdown(
    image_name: str,
    db: AsyncSession = Depends(get_db)
):
    ocr_service = OCRService(db)
    try:
        record = await ocr_service.process_and_store(image_name)
        if record.status == "failed":
            raise HTTPException(status_code=500, detail=f"OCR failed: {record.result_markdown}")
        return record
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
