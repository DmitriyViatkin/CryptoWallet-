import asyncio
import logging
from src.tasks.broker import broker as taskiq_broker

logger = logging.getLogger(__name__)

async def run_worker() -> None:
    logger.info("Starting TaskIQ worker...")

    try:
        await taskiq_broker.startup()
        logger.info("Broker started")

        async for _ in taskiq_broker.listen():
            pass

    except Exception as e:
        logger.exception(f"Worker error: {e}")

    finally:
        await taskiq_broker.shutdown()



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_worker())