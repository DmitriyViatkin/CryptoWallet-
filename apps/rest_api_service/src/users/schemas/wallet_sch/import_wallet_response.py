from pydantic import BaseModel
from typing import Optional




class ImportWalletResponse(BaseModel):
    job_id: str
    status: str = "pending"
