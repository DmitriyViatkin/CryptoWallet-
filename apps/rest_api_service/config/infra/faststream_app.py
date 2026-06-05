



from datetime import datetime, timezone, timedelta
from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue, ExchangeType
from shared.messaging.schemas.password_reset_request_event import PasswordResetRequestEvent
from shared.messaging.rabbit_settings import rabbit_topology

rabbit_router = RabbitRouter()

_exchange = RabbitExchange(
    name=rabbit_topology.exchange_name,
    type=ExchangeType.TOPIC,
    durable=True,
)
_email_queue = RabbitQueue(
    name=rabbit_topology.email_notifications_queue,
    routing_key=rabbit_topology.rk_password_reset,
    durable=True,
)
# Окрема черга для реєстрації — теж прив'язана до _exchange
_registration_queue = RabbitQueue(
    name="auth.notifications.registration",
    routing_key=rabbit_topology.rk_user_registered,
    durable=True,
)

@rabbit_router.subscriber(_email_queue, _exchange)
async def handle_password_reset_email(event: PasswordResetRequestEvent) -> None:
    from src.tasks.email_tasks import send_reset_email_task
    await send_reset_email_task.kiq(
        email=event.email,
        token=event.reset_token,
        user_id=str(event.user_id),
    )

@rabbit_router.subscriber(_registration_queue, _exchange)
async def handle_registration_event(msg: dict) -> None:
    from src.tasks.email_tasks import send_welcome_email_task
    from src.tasks.access_chat import enable_chat_access_task

    user_id = msg.get("user_id")
    eta = datetime.now(timezone.utc) + timedelta(minutes=1)

    await send_welcome_email_task.kiq(to_email=msg.get("email"))
    await enable_chat_access_task.kiq(user_id=user_id
    )