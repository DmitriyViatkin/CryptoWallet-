from datetime import datetime
from .product_base_sch import ProductBaseSch
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProductResponseSch(ProductBaseSch):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
