
from uuid import UUID
from pydantic import BaseModel


class WalletImportRequestEvent(BaseModel):
    job_id: str
    user_id: int
    private_key: str | None = None
