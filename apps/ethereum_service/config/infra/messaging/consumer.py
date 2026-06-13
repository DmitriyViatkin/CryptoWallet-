import json
import asyncio
from aio_pika import connect_robust, ExchangeType
from aio_pika.abc import AbstractIncomingMessage

from ethereum_service.config.infra.base_settings import rabbitmq_settings
from ethereum_service.config.infra.cache.job_store import JobStore


class WalletImportedConsumer:
    EXCHANGE = "crypto.topic"
    QUEUE = "eth.wallet.imported"
    ROUTING_KEY = "eth.wallet.imported"

    def __init__(self, job_store: JobStore) -> None:
        self._job_store = job_store
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        self._task = asyncio.create_task(self._consume())

    async def stop(self) -> None:
        if self._task:
            self._task.cancel()

    async def _consume(self) -> None:
        connection = await connect_robust(rabbitmq_settings.url)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=10)

            exchange = await channel.declare_exchange(
                self.EXCHANGE,
                ExchangeType.TOPIC,
                durable=True,
            )
            queue = await channel.declare_queue(self.QUEUE, durable=True)
            await queue.bind(exchange, routing_key=self.ROUTING_KEY)

            async with queue.iterator() as q:
                async for message in q:
                    async with message.process():
                        await self._handle(message)

    async def _handle(self, message: AbstractIncomingMessage) -> None:
        data = json.loads(message.body)
        job_id = message.correlation_id or data.get("job_id")

        if not job_id:
            return

        if data.get("error"):
            await self._job_store.fail(job_id)
            return

        await self._job_store.complete(job_id, {
            "address": data["address"],
            "user_id": data["user_id"],
        })