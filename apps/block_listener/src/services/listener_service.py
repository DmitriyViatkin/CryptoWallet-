import logging

from redis.asyncio import Redis

from src.core.ws_client import AlchemyWSClient
from src.core.block_parser import parse_block_transactions
from config.infra.messaging.publisher import TxDetectedPublisher

logger = logging.getLogger(__name__)

LAST_BLOCK_KEY = "block_listener:last_processed_block"
ADDRESSES_KEY = "wallets:addresses"


class BlockListenerService:
    def __init__(
        self,
        ws_client: AlchemyWSClient,
        redis: Redis,
        publisher: TxDetectedPublisher,
    ):
        self._ws_client = ws_client
        self._redis = redis
        self._publisher = publisher

    async def handle_block(self, block_number: int):
        """Вызывается на каждый новый блок."""
        our_addresses = await self._redis.smembers(ADDRESSES_KEY)

        if not our_addresses:
            logger.debug(f"Block {block_number}: no addresses to watch, skipping.")
            await self._redis.set(LAST_BLOCK_KEY, block_number)
            return

        txs = await parse_block_transactions(
            w3=self._ws_client.w3,
            block_number=block_number,
            our_addresses=our_addresses,
        )

        for tx in txs:
            await self._publisher.publish_tx_detected(**tx)
            logger.info(f"Published tx_detected: {tx['tx_hash']}")

        # Персистим последний обработанный блок для recovery после рестарта
        await self._redis.set(LAST_BLOCK_KEY, block_number)

    async def run(self):
        """Точка входа — стартует WS-цикл."""
        logger.info("BlockListenerService started.")
        await self._ws_client.listen_new_blocks(self.handle_block)