from pydantic import BaseModel

class WalletCreatedEvent(BaseModel):
    job_id: str
    user_id: int
    title: str
    wallet_type: str
    address: str
    encrypted_private_key: str = ""
    error: str | None = None