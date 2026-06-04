from pydantic import BaseModel, Field
from src.users.schemas.product_sch.product_resp_sch import ProductResponseSch


class ProductListResponseSch(BaseModel):
    items: list[ProductResponseSch]
    total: int = Field(..., description="Общее количество продуктов в базе данных")
    page: int = Field(..., description="Текущая страница")
    size: int = Field(..., description="Количество элементов на странице")