from shared.messaging.rabbit_settings import rabbit_topology
from .broker import broker


@broker.task(queue=rabbit_topology.taskiq_queue)
async def send_reset_email_task(email: str, token: str, user_id: str) -> dict:
    from src.email import send_reset_email_smtp
    await send_reset_email_smtp(to_email=email, reset_token=token)
    return {"status": "sent", "to": email}


@broker.task(queue=rabbit_topology.taskiq_queue)
async def send_welcome_email_task(to_email: str) -> dict:
    from src.email import send_email
    await send_email(
        to_email=to_email,
        subject="Welcome to our service!",
        body="Thank you for registering. We're excited to have you on board!",
    )
    return {"status": "sent", "to": to_email}