from pydantic import BaseModel

class WalletCreateRequestEvent(BaseModel):
    job_id: str
    user_id: int
    title: str
    wallet_type: str