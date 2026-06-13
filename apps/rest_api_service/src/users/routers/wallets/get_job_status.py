from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from src.auth.dependencies import get_current_user
from src.users.models.users import User
from src.users.services.wallet_serv import WalletService
from src.users.schemas.wallet_sch.import_wallet_request import ImportWalletRequest
from src.users.schemas.wallet_sch.import_wallet_response import     ImportWalletResponse
from src.users.schemas.wallet_sch.job_status_response import     JobStatusResponse
from fastapi import Depends

router = APIRouter(route_class=DishkaRoute)


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    service: FromDishka[WalletService],
    current_user: User = Depends(get_current_user),
) -> JobStatusResponse:
    result = await service.get_import_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobStatusResponse(job_id=job_id, **result)


