from uuid import UUID
from pydantic import BaseModel

class WalletImportedEvent(BaseModel):
    job_id: str
    user_id: int
    address: str
    encrypted_private_key: str | None = None
    error: str | None = None