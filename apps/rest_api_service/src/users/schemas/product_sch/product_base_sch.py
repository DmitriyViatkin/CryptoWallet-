from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ProductBaseSch(BaseModel):
    title: str = Field(..., max_length=100)
    wallet_address: str = Field(..., max_length=255)
    price: Decimal