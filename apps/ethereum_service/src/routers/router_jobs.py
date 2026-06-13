from fastapi import APIRouter, HTTPException
from dishka.integrations.fastapi import DishkaRoute, FromDishka

from src.services.ethereum_serv import WalletService
from src.schemas.job_status import JobStatus

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    route_class=DishkaRoute,  # ← це було відсутнє, звідси і падіння
)

@router.get("/{job_id}", response_model=JobStatus)
async def get_job_status(
    job_id: str,
    service: FromDishka[WalletService],
) -> JobStatus:
    result = await service.get_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result