from faststream.asyncapi.schema import operations
from faststream.rabbit import RabbitRouter, RabbitExchange, RabbitQueue, ExchangeType, RabbitBroker
from faststream import Context
from typing import Annotated
from shared.messaging.rabbit_settings import rabbit_topology
from shared.messaging.schemas.wallet.wallet_import_request_event import WalletImportRequestEvent
from shared.messaging.schemas.wallet.wallet_imported_event import WalletImportedEvent
from shared.crypto.encryption import encrypt_private_key
from shared.messaging.schemas.wallet.wallet_created_event import WalletCreatedEvent
from shared.messaging.schemas.wallet.wallet_create_request_event import WalletCreateRequestEvent


rabbit_router = RabbitRouter()

_wallet_create_queue = RabbitQueue(
    name=rabbit_topology.wallet_create_queue,
    routing_key=rabbit_topology.rk_wallet_create,
    durable=True,
)

_exchange = RabbitExchange(
    name=rabbit_topology.exchange_name,
    type=ExchangeType.TOPIC,
    durable=True,
)
_wallet_import_queue = RabbitQueue(
    name=rabbit_topology.wallet_import_queue,
    routing_key=rabbit_topology.rk_wallet_import,
    durable=True,
)


@rabbit_router.subscriber(_wallet_import_queue, _exchange)
async def handle_wallet_import(
    msg: WalletImportRequestEvent,  # FastStream десериализует автоматически
    broker: Annotated[RabbitBroker, Context()],
) -> None:
    print(f"[DEBUG] {msg}")

    # Импорт здесь, чтобы избежать circular import при загрузке модуля
    from config.ioc import container
    from src.services.web3_wallet_service import Web3WalletService

    try:


        async with container() as request_container:  # открываем scope запроса
            service = await request_container.get(Web3WalletService)
            wallet_address = await service.import_wallet(
                private_key=msg.private_key,
            )
            operations = await service.get_transactions(wallet_address)

            reply = WalletImportedEvent(
                job_id=msg.job_id,
                user_id=msg.user_id,
                address=wallet_address,
                encrypted_private_key=encrypt_private_key(msg.private_key),
                operations=operations,
            )
            print(reply)


    except Exception as e:

        print("exception:", repr(e))

        import traceback

        traceback.print_exc()

        reply = WalletImportedEvent(

            job_id=msg.job_id,

            user_id=msg.user_id,

            address="",

            error=str(e),

        )

    await broker.publish(
        reply,
        exchange=_exchange,
        routing_key=rabbit_topology.rk_wallet_imported,
    )

@rabbit_router.subscriber(_wallet_create_queue, _exchange)
async def handle_wallet_create(
    msg: WalletCreateRequestEvent,
    broker: Annotated[RabbitBroker, Context()],
) -> None:
    from config.ioc import container
    from src.services.web3_wallet_service import Web3WalletService

    try:
        async with container() as request_container:
            service = await request_container.get(Web3WalletService)
            address, encrypted_key = await service.create_wallet()

        reply = WalletCreatedEvent(
            job_id=msg.job_id,
            user_id=msg.user_id,
            title=msg.title,
            wallet_type=msg.wallet_type,
            address=address,
            encrypted_private_key=encrypted_key,
        )
    except Exception as e:
        reply = WalletCreatedEvent(
            job_id=msg.job_id,
            user_id=msg.user_id,
            title=msg.title,
            wallet_type=msg.wallet_type,
            address="",
            error=str(e),
        )

    await broker.publish(
        reply,
        exchange=_exchange,
        routing_key=rabbit_topology.rk_wallet_created,
    )


