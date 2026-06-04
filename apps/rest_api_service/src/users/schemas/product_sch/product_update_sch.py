from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class ProductUpdateSch(BaseModel):
    product_id: int= Field(None, description="Id продукта")
    title: Optional[str] = Field(None, max_length=100)
    wallet_address: Optional[str] = Field(None, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)