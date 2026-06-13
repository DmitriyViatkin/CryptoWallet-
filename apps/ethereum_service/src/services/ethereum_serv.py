from uuid import uuid4, UUID

from ethereum_service.src.schemas.import_wallet_request  import ImportWalletRequest
from ethereum_service.src.schemas.job_status import JobStatus
from ethereum_service.config.infra.messaging.publisher import WalletEventPublisher
from ethereum_service.config.infra.cache.job_store import JobStore


class WalletService:
    def __init__(
        self,
        publisher: WalletEventPublisher,
        job_store: JobStore,
    ) -> None:
        self._publisher = publisher
        self._job_store = job_store

    async def import_wallet(self, dto: ImportWalletRequest) -> str:
        job_id = str(uuid4())

        await self._job_store.create(job_id)  # статус: pending
        await self._publisher.publish_import_request(
            job_id=job_id,
            user_id=str(dto.user_id),
            private_key=dto.private_key,

        )
        return job_id

    async def get_job(self, job_id: str) -> JobStatus | None:
        return await self._job_store.get(job_id)