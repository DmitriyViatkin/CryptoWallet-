from fastapi import APIRouter, Depends, HTTPException, status

from dishka.integrations.fastapi import FromDishka, inject
from src.auth.services.auth_serv import AuthService
from src.users.services.user_serv import UserService
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.schemas.users.user_update_sch import UpdateUserRequest

router = APIRouter()

@router.patch("/change", response_model = UpdateUserRequest )
@inject
async def update_me(
        body:UpdateUserRequest,
        user_service: FromDishka[UserService],
        auth_service: FromDishka[AuthService],
        current_user: User = Depends(get_current_user),

):


     if body.new_password and not body.current_password:
        raise HTTPException(
             status_code= status.HTTP_400_BAD_REQUEST,
             detail = "Current password is required to set a new one"
         )
     if body.current_password:
         if not auth_service.verify_password(body.current_password, current_user.hashed_password):
             raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST,
                                 detail="Current password is incorrect",)

     update_data= body.model_dump(exclude_unset=True)
     update_data.pop("current_password", None)
     if "new_password" in update_data:
            update_data["new_password"] = auth_service.hash_password(
                update_data["new_password"])
     try:
         updated_user = await user_service.update_profile(
             user_id= current_user.id,
             **update_data
         )
     except ValueError as e:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

     if not updated_user:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="User not found")

     return updated_user
