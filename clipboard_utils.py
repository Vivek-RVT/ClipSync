from cryptography.fernet import Fernet, InvalidToken
import hashlib

def password_to_key(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key[:32]))

import base64

def encrypt_data(data: str, password: str) -> bytes:
    f = password_to_key(password)
    return f.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes, password: str) -> str:
    try:
        f = password_to_key(password)
        return f.decrypt(encrypted_data).decode()
    except InvalidToken:
        raise Exception("❌ Invalid password or corrupted data")
