from uuid import UUID
from typing import Optional, Literal
from pydantic import BaseModel, Field

class WalletResult(BaseModel):

    address: str
    user_id: UUID
