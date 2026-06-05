import asyncio
import logging

from src.tasks.broker import broker as taskiq_broker

logger = logging.getLogger(__name__)


async def run_worker() -> None:
    """
    Worker запускає тільки TaskIQ.
    FastStream subscribers працюють всередині FastAPI процесу
    через RabbitProvider (той самий broker інстанс).

    Якщо потрібен окремий процес для consumers —
    створити окремий entrypoint з власним broker інстансом.
    """
    logger.info("Starting TaskIQ worker...")
    async with taskiq_broker:
        try:
            await taskiq_broker.listen()
        except (KeyboardInterrupt, asyncio.CancelledError):
            logger.info("Worker shutdown")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_worker())