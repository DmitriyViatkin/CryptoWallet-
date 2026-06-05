from taskiq import TaskiqMiddleware
from taskiq.abc import result_backend
from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

# Імпортуємо налаштування інфраструктури та топологію RabbitMQ для синхронізації назв exchange
from config.infra.config.base_settings import get_infra_settings
from shared.messaging.rabbit_settings import rabbit_topology

settings = get_infra_settings()

def create_broker() -> AioPikaBroker:
    """
    Ініціалізує та налаштовує брокер Taskiq для асинхронного виконання завдань.
    
    Використовує RabbitMQ (через AioPika) як транспорт для повідомлень 
    та Redis як сховище для результатів виконання завдань.
    """
    
    # Налаштовуємо Redis для збереження результатів (чи успішно виконане завдання, що повернуло тощо)
    redis_backend = RedisAsyncResultBackend(
        redis_url=settings.redis.url,  # "redis://:password@host:port/1"
    )

    # Налаштовуємо основний брокер RabbitMQ
    # Використовуємо параметри з rabbit_topology для забезпечення єдиної конфігурації в проекті
    broker = AioPikaBroker(
        url=settings.rabbitmq.url,
        exchange_name=rabbit_topology.taskiq_exchange_name,
        exchange_type=rabbit_topology.taskiq_exchange_type,
        declare_exchange_kwargs={"durable": True},  # ← ось так
        declare_queues_kwargs={"durable": True},  # черги теж зробимо durable
        qos=10,
    ).with_result_backend(redis_backend)
    
    return broker

# Створюємо глобальний екземпляр брокера, який буде використовуватись воркерами та API
broker = create_broker()
