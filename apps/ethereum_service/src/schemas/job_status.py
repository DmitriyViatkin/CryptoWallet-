from .wallet_result import WalletResult
from typing import Optional, Literal
from pydantic import BaseModel, Field

class JobStatus(BaseModel):

    job_id: str
    status: Literal ["pending", "done", "failed"]
    result: Optional[WalletResult] = None