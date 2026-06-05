from datetime import datetime, timezone
from sqlalchemy import update
from shared.messaging.rabbit_settings import rabbit_topology
from src.database import AsyncSessionLocal
from .broker import broker
from ..users.models.permissions import Permission

@broker.task(queue=rabbit_topology.chat_access_queue)
async def enable_chat_access_task(user_id: int):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = (
                update(Permission)
                .where(Permission.user_id == user_id)
                .values(has_chat_access=True)
            )
            await session.execute(stmt)
    return {
        "status": "success",
        "user_id": user_id,
        "activated_at": str(datetime.now(timezone.utc)),
    }