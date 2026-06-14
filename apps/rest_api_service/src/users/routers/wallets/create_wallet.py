from fastapi import APIRouter, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.import_wallet_response import ImportWalletResponse
from src.users.schemas.wallet_sch.create_import_sch import CreateWalletRequest
from fastapi import Depends

router = APIRouter(route_class=DishkaRoute)


@router.post("/create", status_code=status.HTTP_202_ACCEPTED, response_model=ImportWalletResponse)
async def create_wallet(
    body: CreateWalletRequest,
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
) -> ImportWalletResponse:
    job_id = await service.request_wallet_create(
        user_id=current_user.id,
        title=body.title,
    )
    return ImportWalletResponse(job_id=job_id)