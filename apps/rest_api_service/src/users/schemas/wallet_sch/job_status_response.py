from pydantic import BaseModel
from typing import Optional

class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # pending | done | failed
    address: Optional[str] = None
    error: Optional[str] = None
    