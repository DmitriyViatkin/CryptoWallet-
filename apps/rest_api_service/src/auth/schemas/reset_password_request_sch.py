from pydantic import BaseModel, EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str