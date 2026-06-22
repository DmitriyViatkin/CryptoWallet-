from faststream.rabbit import RabbitBroker, RabbitExchange, ExchangeType

from shared.messaging.rabbit_settings import rabbit_topology
from shared.messaging.schemas.tx_detected_event import TxDetectedEvent

_exchange = RabbitExchange(
    name=rabbit_topology.exchange_name,
    type=ExchangeType.TOPIC,
    durable=True,
)

class TxDetectedPublisher:

    def __init__(self, broker: RabbitBroker):
        self._broker = broker

    async def publish_tx_detected(self, **kwargs):
        event = TxDetectedEvent(**kwargs)
        await self._broker.publish(
            event,
            exchange=_exchange,
            routing_key=rabbit_topology.rk_tx_detected,)