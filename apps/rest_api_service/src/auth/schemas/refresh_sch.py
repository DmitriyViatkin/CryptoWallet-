from pydantic import BaseModel, EmailStr

class RefreshRequest(BaseModel):
    refresh_token: str


 