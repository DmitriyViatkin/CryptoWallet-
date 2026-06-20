from pydantic import BaseModel

class WalletSentTransEvent(BaseModel):
    job_id: str
    tx_hash: str | None = None
    error: str | None = None