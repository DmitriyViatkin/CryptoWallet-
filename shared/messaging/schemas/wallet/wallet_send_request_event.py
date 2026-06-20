




from pydantic import BaseModel

class WalletSendTransEvent(BaseModel):
    job_id: str
    encrypted_private_key: str
    address_from: str
    address_to: str
    amount: float