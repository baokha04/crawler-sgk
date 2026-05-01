import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from app.core.security import encrypt_3des, decrypt_3des
from app.domains.config.service import ConfigService
from app.infrastructure.database import AsyncSessionLocal, init_db
from app.infrastructure.models import Config
from sqlalchemy.future import select

async def test_encryption():
    print("Testing 3DES Encryption...")
    original = "AIzaSyTestKey123456"
    encrypted = encrypt_3des(original)
    decrypted = decrypt_3des(encrypted)
    
    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    
    assert original == decrypted, "Encryption/Decryption failed!"
    print("Encryption test passed!")

async def test_config_service():
    print("\nTesting ConfigService...")
    await init_db()
    
    async with AsyncSessionLocal() as session:
        service = ConfigService(session)
        
        # Set config
        key = "google_api_key"
        val = "AIzaSyDatabaseKey"
        await service.set_config(key, val)
        
        # Verify active config
        active_val = await service.get_active_config(key)
        print(f"Active value in DB: {active_val}")
        assert active_val == val, "ConfigService retrieval failed!"
        
        # Verify encryption in DB
        result = await session.execute(select(Config).where(Config.key == key, Config.active == 1))
        config_row = result.scalars().first()
        print(f"Raw value in DB (should be encrypted): {config_row.value}")
        assert config_row.value != val, "Value not encrypted in database!"
        
        # Test switching active config
        new_val = "AIzaSyNewActiveKey"
        await service.set_config(key, new_val)
        
        active_val = await service.get_active_config(key)
        print(f"New active value: {active_val}")
        assert active_val == new_val
        
        # Verify previous one is inactive
        result = await session.execute(select(Config).where(Config.key == key, Config.active == 0))
        inactive_configs = result.scalars().all()
        print(f"Number of inactive configs: {len(inactive_configs)}")
        assert len(inactive_configs) >= 1
        
    print("ConfigService test passed!")

if __name__ == "__main__":
    asyncio.run(test_encryption())
    asyncio.run(test_config_service())
