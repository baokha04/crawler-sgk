from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad
import base64
from app.core.config import settings

def encrypt_3des(text: str) -> str:
    if not text:
        return ""
    key = settings.DES3_KEY.encode('utf-8')
    # 3DES block size is 8 bytes
    cipher = DES3.new(key, DES3.MODE_ECB)
    padded_data = pad(text.encode('utf-8'), DES3.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_data).decode('utf-8')

def decrypt_3des(encrypted_text: str) -> str:
    if not encrypted_text:
        return ""
    try:
        key = settings.DES3_KEY.encode('utf-8')
        cipher = DES3.new(key, DES3.MODE_ECB)
        decoded_data = base64.b64decode(encrypted_text)
        decrypted_data = cipher.decrypt(decoded_data)
        return unpad(decrypted_data, DES3.block_size).decode('utf-8')
    except Exception:
        # Return as is if decryption fails (might not be encrypted)
        return encrypted_text
