from uuid import UUID
from pydantic import BaseModel
from .wallet_operation_data import WalletOperation

class WalletImportedEvent(BaseModel):
    job_id: str
    user_id: int
    address: str
    encrypted_private_key: str | None = None
    operations: list[WalletOperation] = []
    error: str | None = None