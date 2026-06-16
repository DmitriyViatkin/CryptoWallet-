from pydantic import BaseModel, Field
from decimal import Decimal
from enums import OperationType


class GetTransactionsWalletRequestSch(BaseModel):

    wallet_id: int

class GetTransactionsWalletResponseSch(BaseModel):

    wallet_id :int
    tx_hash : str
    from_address : str
    to_address : str
    amount: Decimal
    operation_type: OperationType

    model_config =  {
        "from_attributes": True
    }

class TransactionsListResponseSch(BaseModel):
    items: list[GetTransactionsWalletResponseSch]
    total: int = Field(..., description="Загальна кількість елементів")
    page: int = Field(..., description="Поточна сторінка")
    size: int = Field(..., description="Кількість елементів на сторінці")