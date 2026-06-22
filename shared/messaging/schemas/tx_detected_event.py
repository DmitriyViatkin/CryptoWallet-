from decimal import Decimal

from pydantic import BaseModel, field_serializer


class TxDetectedEvent(BaseModel):
    """
    Подія, яка публікується block_listener при виявленні транзакції,
    що стосується одного з наших гаманців (адреса from або to входить
    до списку our_addresses).
    """

    tx_hash: str
    from_address: str
    to_address: str | None = None
    amount: Decimal
    block_number: int
    status: str  # "completed" | "failed"

    @field_serializer("amount")
    def serialize_amount(self, amount: Decimal) -> str:
        """
        Сериализуем Decimal как строку, а не как float/number.

        Если этого не сделать, pydantic при сериализации в JSON для RabbitMQ
        может потерять точность (float не умеет точно хранить произвольную
        десятичную дробь) — для денежных сумм это критично.
        auth_service при десериализации должен явно делать Decimal(value),
        а не полагаться на автоматическое приведение типа.
        """
        return str(amount)