from config.infra.providers.rabbit_broker import broker
from config.infra.builder import FastStreamBuilder

builder = FastStreamBuilder(
    broker=broker,
    title="block_listener",
    description="Слушает блоки Sepolia через Alchemy WS, детектит tx по нашим адресам",
)

app = builder.get_app()