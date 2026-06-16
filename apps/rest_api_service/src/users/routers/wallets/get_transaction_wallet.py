from fastapi import APIRouter, status, Depends, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.get_tansaction_response_sch import (
    GetTransactionsWalletResponseSch,
    GetTransactionsWalletRequestSch, TransactionsListResponseSch)


router = APIRouter(route_class=DishkaRoute)

@router.get("/transactions", status_code=status.HTTP_200_OK,
            response_model= TransactionsListResponseSch)
async def get_transactions(
    wallet_id: int,
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
):
    wallet = await service.get_by_id(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    operations = await service.get_wallet_operations(wallet_id=wallet_id)
    return TransactionsListResponseSch(
            items=operations,
            total=len(operations),
            page=1,
            size=len(operations),
        )



