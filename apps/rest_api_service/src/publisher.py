from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType

from shared.messaging.rabbit_settings import rabbit_topology
from shared.messaging.schemas.password_reset_request_event import PasswordResetRequestEvent
from shared.messaging.schemas.user_register_event import UserRegisteredEvent
from shared.messaging.schemas.wallet.wallet_import_request_event import WalletImportRequestEvent

_exchange = RabbitExchange(
    name=rabbit_topology.exchange_name,
    type=ExchangeType.TOPIC,
    durable=True,
)


class EventPublisher:
    def __init__(self, broker: RabbitBroker) -> None:
        self._broker = broker

    async def publish_password_reset(
        self,
        to_email: str,
        reset_token: str,
        user_id: int,
    ) -> None:
        event = PasswordResetRequestEvent(
            email=to_email,
            reset_token=reset_token,
            user_id=str(user_id),
        )
        await self._broker.publish(
            event,
            exchange=_exchange,
            routing_key=rabbit_topology.rk_password_reset,
        )

    async def publish_user_registered(self, user_id: int, email: str) -> None:
        event = UserRegisteredEvent(
            user_id=str(user_id),
            email=email,
        )
        await self._broker.publish(
            event,
            exchange=_exchange,
            routing_key=rabbit_topology.rk_user_registered,
        )

    async def publish_wallet_import(
            self,
            job_id: str,
            user_id: int,
            private_key: str | None,

    ) -> None:
        event = WalletImportRequestEvent(
            job_id=job_id,
            user_id=user_id,
            private_key=private_key,
             
        )
        await self._broker.publish(
            event,
            exchange=_exchange,
            routing_key=rabbit_topology.rk_wallet_import,
        )