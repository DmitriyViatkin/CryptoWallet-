from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.import_wallet_request import ImportWalletRequest
from src.users.schemas.wallet_sch.import_wallet_response import ImportWalletResponse
from src.users.schemas.wallet_sch.job_status_response import JobStatusResponse
from fastapi import Depends

router = APIRouter(route_class=DishkaRoute)


@router.post("/import", status_code=status.HTTP_202_ACCEPTED, response_model=ImportWalletResponse)
async def import_wallet(
    body: ImportWalletRequest,
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
) -> ImportWalletResponse:
    job_id = await service.request_wallet_import(
        user_id=current_user.id,
        private_key=body.private_key,
    )
    return ImportWalletResponse(job_id=job_id)


