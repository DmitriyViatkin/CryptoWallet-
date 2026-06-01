from sqlalchemy import Column, Integer, String, DateTime,   ForeignKey, Numeric, func
from sqlalchemy.orm import relationship

from apps.rest_api_service.src.database import Base


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    wallet_address = Column(String(255), nullable=False)
    price = Column(Numeric(38, 18), nullable=False)
    created_at = Column(DateTime, default=func.now())

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="products")
    order_items = relationship("OrderItems", back_populates="product")