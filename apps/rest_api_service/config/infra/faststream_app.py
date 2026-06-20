"""
 Модуль конфигурации FastStream для работы с RabbitMQ.
 Определяет маршрутизацию событий, очереди и обработчики (subscribers)
 для асинхронного взаимодействия между сервисами.
 """

from datetime import datetime, timezone, timedelta

from aiohttp import payload
from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue, ExchangeType

# Импорт схем сообщений и настроек топологии
from shared.messaging.schemas.password_reset_request_event import \
    PasswordResetRequestEvent
from shared.messaging.schemas.user_register_event import UserRegisteredEvent
from shared.messaging.rabbit_settings import rabbit_topology
from shared.messaging.schemas.wallet.wallet_imported_event import WalletImportedEvent
from shared.messaging.schemas.wallet.wallet_created_event import WalletCreatedEvent
from shared.messaging.schemas.wallet.wallet_send_request_event import WalletSendTransEvent
from shared.messaging.schemas.wallet.wallet_send_event import WalletSentTransEvent



# Инициализация роутера RabbitMQ
rabbit_router = RabbitRouter()

# Настройка основного обменника (Exchange) типа TOPIC
_exchange = RabbitExchange(
    name=rabbit_topology.exchange_name,
    type=ExchangeType.TOPIC,
    durable=True,
)
_wallet_created_queue = RabbitQueue(
    name=rabbit_topology.wallet_created_queue,
    routing_key=rabbit_topology.rk_wallet_created,
    durable=True,
)
# Очередь для уведомлений о сбросе пароля
_email_queue = RabbitQueue(
    name=rabbit_topology.email_notifications_queue,
    routing_key=rabbit_topology.rk_password_reset,
    durable=True,
)

# Очередь для обработки регистрации новых пользователей
_registration_queue = RabbitQueue(
    name="auth.notifications.registration",
    routing_key=rabbit_topology.rk_user_registered,
    durable=True,
)

# Очередь для получения результатов импорта кошельков
_wallet_imported_queue = RabbitQueue(
    name=rabbit_topology.wallet_imported_queue,
    routing_key=rabbit_topology.rk_wallet_imported, durable=True)

# Черги для транзакцій
_wallet_send_trans_queue = RabbitQueue(
    name=rabbit_topology.wallet_send_trans_queue,
    routing_key=rabbit_topology.rk_send_trans,
    durable=True,
)
_wallet_sent_trans_queue = RabbitQueue(
    name=rabbit_topology.wallet_sent_trans_queue,
    routing_key=rabbit_topology.rk_sent_trans,
    durable=True,
)




@rabbit_router.subscriber(_email_queue, _exchange)
async def handle_password_reset_email(event: PasswordResetRequestEvent) -> None:
    """
    Обработчик события запроса на сброс пароля.
    Ставит задачу в Taskiq для отправки письма пользователю.
    """
    # Импорты внутри функций используются для предотвращения циклической зависимости
    from src.tasks.email_tasks import send_reset_email_task

    await send_reset_email_task.kiq(
        email=event.email,
        token=event.reset_token,
        user_id=str(event.user_id),
    )


@rabbit_router.subscriber(_registration_queue, _exchange)
async def handle_registration_event(event: UserRegisteredEvent) -> None:
    """
    Обработчик события успешной регистрации.
    Отправляет приветственное письмо и активирует доступ к чату.
    """
    from src.tasks.email_tasks import send_welcome_email_task
    from src.tasks.access_chat import enable_chat_access_task

    await send_welcome_email_task.kiq(to_email=event.email)
    await enable_chat_access_task.kiq(
        user_id=event.user_id
    )


@rabbit_router.subscriber(_wallet_imported_queue, _exchange)
async def handle_wallet_imported(event: WalletImportedEvent) -> None:
    """
    Обработчик завершения импорта кошелька.
    Сохраняет результат операции в Redis, чтобы фронтенд мог
    получить статус задачи по job_id.
    """


    from config.ioc import container
    from redis.asyncio import Redis
    from src.users.services.wallet_serv import WalletService
    import json

    if event.error:

        payload = {"status": "failed", "error": event.error}
    else:
        payload = {"status": "done", "address": event.address}

    async with container() as request_container:

        # Получаем экземпляр Redis из DI-контейнера
        redis: Redis = await request_container.get(Redis)
        await redis.setex(
            f"job:{event.job_id}",
            300, json.dumps(payload) ) # TTL 5 минут
        if not event.error:
            wallet_service: WalletService = await request_container.get(WalletService)
            await wallet_service.import_wallet(
                user_id=event.user_id,
                wallet_address=event.address,
                encrypted_private_key=event.encrypted_private_key or "",
                operations=event.operations,
            )

@rabbit_router.subscriber(_wallet_created_queue, _exchange)
async def handle_wallet_created(event: WalletCreatedEvent) -> None:
    from config.ioc import container
    from redis.asyncio import Redis
    from src.users.services.wallet_serv import WalletService
    import json

    if event.error:
        payload = {"status": "failed", "error": event.error}
    else:
        payload = {"status": "done", "address": event.address}

    async with container() as request_container:
        redis: Redis = await request_container.get(Redis)
        await redis.setex(f"job:{event.job_id}", 300, json.dumps(payload))

        if not event.error:
            wallet_service: WalletService = await request_container.get(
                WalletService)
            await wallet_service.create_wallet(
                user_id=event.user_id,
                title=event.title,
                wallet_address=event.address,
                encrypted_private_key=event.encrypted_private_key,
            )

    @rabbit_router.subscriber(_wallet_sent_trans_queue, _exchange)
    async def handle_wallet_sent_trans(event: WalletSentTransEvent) -> None:
        from config.ioc import container
        from redis.asyncio import Redis
        import json

        if event.error:
            payload = {"status": "failed", "error": event.error}
        else:
            payload = {"status": "done", "tx_hash": event.tx_hash}

        async with container() as request_container:
            redis: Redis = await request_container.get(Redis)
            await redis.setex(f"job:{event.job_id}", 300, json.dumps(payload))