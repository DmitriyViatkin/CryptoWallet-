from fastapi import APIRouter, status, Depends, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.get_tansaction_response_sch import (
    GetTransactionsWalletResponseSch,
    GetTransactionsWalletRequestSch, TransactionsListResponseSch)


router = APIRouter(route_class=DishkaRoute)

@router.get("/transaction", status_code=status.HTTP_200_OK,
            response_model= GetTransactionsWalletResponseSch)
async def get_transaction(
    tx_hash: str,
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
):


    trans = await service.get_operation_by_tx(tx_hash=tx_hash)
    if not trans:
        raise HTTPException(status_code=404, detail="Transaction not found")


    return  trans