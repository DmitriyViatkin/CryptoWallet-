import asyncio
import logging

from config.infra.faststream_app import app
from config.ioc import container
from src.services.listener_service import BlockListenerService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s - %(message)s",
)

listener_task: asyncio.Task | None = None


@app.on_startup
async def start_listener():
    global listener_task
    service = await container.get(BlockListenerService)  # без async with — важно!
    listener_task = asyncio.create_task(service.run())


@app.on_shutdown
async def stop_listener():
    if listener_task:
        listener_task.cancel()
    await container.close()