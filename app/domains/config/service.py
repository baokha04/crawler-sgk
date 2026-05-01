from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from app.infrastructure.models import Config
from app.core.security import encrypt_3des, decrypt_3des
from typing import Optional, List
from datetime import datetime

class ConfigService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_active_config(self, key: str) -> Optional[str]:
        result = await self.db.execute(
            select(Config).where(Config.key == key, Config.active == 1)
            .order_by(Config.created_at.desc())
        )
        config = result.scalars().first()
        if config:
            return decrypt_3des(config.value)
        return None

    async def set_config(self, key: str, value: str, active: bool = True):
        # Deactivate previous configs if this one is active
        if active:
            await self.deactivate_all(key)
        
        encrypted_value = encrypt_3des(value)
        new_config = Config(
            key=key,
            value=encrypted_value,
            active=1 if active else 0
        )
        self.db.add(new_config)
        await self.db.commit()
        await self.db.refresh(new_config)
        return new_config

    async def deactivate_all(self, key: str):
        await self.db.execute(
            update(Config)
            .where(Config.key == key)
            .values(active=0)
        )
        await self.db.commit()

    async def list_configs(self) -> List[Config]:
        result = await self.db.execute(select(Config).order_by(Config.key, Config.created_at.desc()))
        return result.scalars().all()

    async def update_config(self, config_id: int, value: Optional[str] = None, active: Optional[bool] = None) -> Optional[Config]:
        result = await self.db.execute(select(Config).where(Config.id == config_id))
        config = result.scalars().first()
        if not config:
            return None
        
        if value is not None:
            config.value = encrypt_3des(value)
        if active is not None:
            if active and config.active == 0:
                await self.deactivate_all(config.key)
            config.active = 1 if active else 0
            
        config.updated_at = datetime.utcnow()
        await self.db.commit()
        await self.db.refresh(config)
        return config
