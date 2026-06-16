from fastapi import APIRouter, status, Depends, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.all_wallets_user_sch import AllWalletsResponse


router = APIRouter(route_class=DishkaRoute)

@router.get("/all_wallets", status_code=status.HTTP_200_OK,
            response_model= AllWalletsResponse)
async def get_transaction(
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
):


    wallets = await service.get_user_wallets(user_id=current_user.id)

    if not wallets:
        raise HTTPException(status_code=404, detail="Wallet not found")




    return  AllWalletsResponse(items=wallets)