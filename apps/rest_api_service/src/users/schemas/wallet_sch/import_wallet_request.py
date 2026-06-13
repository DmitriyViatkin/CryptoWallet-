from pydantic import BaseModel
from typing import Optional


class ImportWalletRequest(BaseModel):
    private_key: Optional[str] = None
    #mnemonic: Optional[str] = None
    #title: str
