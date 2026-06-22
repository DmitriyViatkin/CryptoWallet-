import asyncio
import logging

from web3 import AsyncWeb3
from web3.providers.persistent import WebSocketProvider

logger = logging.getLogger(__name__)


class AlchemyWSClient:
    def __init__(self, ws_url: str, reconnect_delay: int = 5, max_delay: int = 60):
        self._ws_url = ws_url
        self._reconnect_delay = reconnect_delay
        self._max_delay = max_delay
        self.w3: AsyncWeb3 | None = None

    async def listen_new_blocks(self, on_block):
        """
        Бесконечный цикл: подключается к Alchemy WS, подписывается на newHeads,
        при каждом новом блоке вызывает on_block(block_number).
        При разрыве соединения — переподключается с экспоненциальным backoff.
        """
        delay = self._reconnect_delay

        while True:
            try:
                logger.info("Connecting to Alchemy WS...")
                async with AsyncWeb3(WebSocketProvider(self._ws_url)) as w3:
                    self.w3 = w3
                    logger.info("WS connected. Subscribing to newHeads...")
                    delay = self._reconnect_delay  # сброс backoff после успешного подключения

                    await w3.eth.subscribe("newHeads")

                    async for block_header in w3.socket.process_subscriptions():
                        number = block_header["result"]["number"]
                        block_number = int(number, 16) if isinstance(number, str) else number
                        logger.info(f"New block: {block_number}")
                        await on_block(block_number)

            except asyncio.CancelledError:
                # Сервис останавливается штатно — выходим без retry
                logger.info("WS listener cancelled, shutting down.")
                return

            except Exception as e:
                logger.warning(f"WS connection lost: {e}. Reconnecting in {delay}s...")
                self.w3 = None
                await asyncio.sleep(delay)
                delay = min(delay * 2, self._max_delay)  # экспоненциальный backoff