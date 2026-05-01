from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies.database import get_db
from app.domains.config.service import ConfigService
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class ConfigSchema(BaseModel):
    id: int
    key: str
    active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ConfigCreate(BaseModel):
    key: str
    value: str
    active: bool = True

@router.get("/", response_model=List[ConfigSchema])
async def list_configs(db: AsyncSession = Depends(get_db)):
    service = ConfigService(db)
    return await service.list_configs()

@router.get("/{key}/active")
async def get_active_config(key: str, db: AsyncSession = Depends(get_db)):
    service = ConfigService(db)
    value = await service.get_active_config(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Active config not found")
    return {"key": key, "value": value}

@router.post("/", response_model=ConfigSchema)
async def set_config(config: ConfigCreate, db: AsyncSession = Depends(get_db)):
    service = ConfigService(db)
    return await service.set_config(config.key, config.value, config.active)
