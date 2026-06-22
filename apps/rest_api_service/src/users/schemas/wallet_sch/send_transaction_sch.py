from pydantic import BaseModel

class SendTransactionRequest(BaseModel):
    """Те, що надсилає користувач у HTTP-запиті."""
    wallet_id: int
    address_to: str
    amount: float


class SendTransactionResponse(BaseModel):
    """Те, що повертається користувачу у відповідь."""
    job_id: str