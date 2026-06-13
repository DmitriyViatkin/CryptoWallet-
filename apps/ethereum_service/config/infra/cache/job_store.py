from redis.asyncio import Redis
from ethereum_service.src.schemas.job_status import JobStatus


JOB_TTL = 300  # 5 хвилин


class JobStore:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def create(self, job_id: str) -> None:
        payload = JobStatus(job_id=job_id, status="pending")
        await self._redis.setex(
            f"job:{job_id}",
            JOB_TTL,
            payload.model_dump_json(),
        )

    async def complete(self, job_id: str, result: dict) -> None:
        from ethereum_service.src.schemas.wallet_result import WalletResult
        payload = JobStatus(
            job_id=job_id,
            status="done",
            result=WalletResult(**result),
        )
        await self._redis.setex(
            f"job:{job_id}",
            JOB_TTL,
            payload.model_dump_json(),
        )

    async def fail(self, job_id: str) -> None:
        payload = JobStatus(job_id=job_id, status="failed")
        await self._redis.setex(f"job:{job_id}", JOB_TTL, payload.model_dump_json())

    async def get(self, job_id: str) -> JobStatus | None:
        raw = await self._redis.get(f"job:{job_id}")
        if not raw:
            return None
        return JobStatus.model_validate_json(raw)