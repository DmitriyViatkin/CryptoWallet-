from cryptography.fernet import Fernet
import os

_KEY = os.environ["WALLET_ENCRYPTION_KEY"]  # base64 ключ, сгенерированный Fernet.generate_key()
_fernet = Fernet(_KEY.encode())

def encrypt_private_key(private_key: str) -> str:
    return _fernet.encrypt(private_key.encode()).decode()

def decrypt_private_key(encrypted: str) -> str:
    return _fernet.decrypt(encrypted.encode()).decode()