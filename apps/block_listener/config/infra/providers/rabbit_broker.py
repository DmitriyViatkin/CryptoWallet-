from faststream.rabbit import RabbitBroker

from config.infra.base_settings import rabbitmq_settings

broker = RabbitBroker(url=rabbitmq_settings.url)