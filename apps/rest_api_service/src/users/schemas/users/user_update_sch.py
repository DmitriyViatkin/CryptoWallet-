from pydantic import BaseModel, EmailStr
from typing  import Optional

class UpdateUserRequest(BaseModel):

    username:Optional[str]= None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    is_active: Optional[bool] = None