from fastapi import APIRouter, status, Depends, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.auth.dependencies import get_current_user
from src.users.schemas.wallet_sch.send_transaction_sch import SendTransactionRequest, \
    SendTransactionResponse


router = APIRouter(route_class=DishkaRoute)

@router.post("/send_transaction", status_code=status.HTTP_202_ACCEPTED,
             response_model=SendTransactionResponse)
async def send_transaction(body: SendTransactionRequest,
                           service: FromDishka[WalletService],
                           current_user: User = Depends(get_current_user)):
    job_id = await service.request_send_transaction(
        user_id=current_user.id,
        wallet_id=body.wallet_id,
        address_to=body.address_to,
        amount=body.amount
    )
    return SendTransactionResponse(job_id=job_id)