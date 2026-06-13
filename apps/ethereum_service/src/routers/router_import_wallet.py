from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from pydantic import BaseModel
from typing import Optional

from ethereum_service.src.services.ethereum_serv import  WalletService
from ethereum_service.src.schemas.import_wallet_request import ImportWalletRequest
from ethereum_service.src.schemas.job_status import JobStatus
from ethereum_service.src.schemas.import_wallet_response import ImportWalletResponse



router = APIRouter(prefix=" ", tags=[""], route_class=DishkaRoute)




@router.post("/import", status_code=status.HTTP_202_ACCEPTED, response_model=ImportWalletResponse)
async def import_wallet(
    body: ImportWalletRequest,
    service: FromDishka[WalletService],
) -> ImportWalletResponse:
    job_id = await service.import_wallet(
        ImportWalletRequest(**body.model_dump())
    )
    return ImportWalletResponse(job_id=job_id)


@router.get("/jobs/{job_id}", response_model=JobStatus)
async def get_job_status(
    job_id: str,
    service: FromDishka[WalletService],
) -> JobStatus:
    result = await service.get_job(job_id)
    if not result:
        raise HTTPException(status_code=404, detail="Job not found")
    return result