from pydantic import BaseModel, Field
from enums import WalletType
from datetime import datetime


# 1. Что мы ждем от клиента при создании
class CreateWalletRequest(BaseModel):
    title: str = Field(..., max_length=100, description="Название кошелька")
    wallet_type: WalletType



# 2. Что мы отдаем клиенту в ответ
class CreateWalletResponse(BaseModel):
    id: int  # Добавили ID из базы
    title: str
    wallet_type: WalletType
    address: str
    created_at: datetime  # Добавили дату создания

    # Приватный ключ (private_key) ТУТ ОТСУТСТВУЕТ ради безопасности

    class Config:
        # Включаем поддержку ORM, чтобы Pydantic умел читать объекты SQLAlchemy
        # (Для Pydantic v2 используется from_attributes = True)
        from_attributes = True