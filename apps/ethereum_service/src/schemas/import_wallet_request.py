from uuid import UUID
from typing import Optional, Literal
from pydantic import BaseModel, Field

class ImportWalletRequest(BaseModel):

    user_id: UUID
    private_key: Optional[str] = None
    #mnemonic: Optional[str] = None