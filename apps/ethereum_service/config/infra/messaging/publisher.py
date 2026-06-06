import json
from aio_pika import connect_robust, ExchangeType, Message
from ethereum_service.config.infra.base_settings import rabbitmq_settings


class WalletEventPublisher:
    EXCHANGE = "crypto.topic"

    async def publish_import_request(
        self,
        job_id: str,
        user_id: str,
        private_key: str | None,
        mnemonic: str | None,
    ) -> None:
        connection = await connect_robust(rabbitmq_settings.url)
        async with connection:
            channel = await connection.channel()
            exchange = await channel.declare_exchange(
                self.EXCHANGE,
                ExchangeType.TOPIC,
                durable=True,
            )
            body = json.dumps({
                "job_id": job_id,
                "user_id": str(user_id),
                "private_key": private_key,
                "mnemonic": mnemonic,
            }).encode()

            await exchange.publish(
                Message(
                    body=body,
                    content_type="application/json",
                    correlation_id=job_id,     # ← для трекінгу
                    reply_to="eth.wallet.imported",  # ← куди відповідати
                ),
                routing_key="eth.wallet.import",
            )