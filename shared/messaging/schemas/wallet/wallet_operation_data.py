from pydantic import BaseModel
from decimal import Decimal

class WalletOperation(BaseModel):

    tx_hash: str
    from_address: str
    to_address: str
    amount: Decimal
    operation_type: str
    status: str = "completed"
    block_number: int | None = None
