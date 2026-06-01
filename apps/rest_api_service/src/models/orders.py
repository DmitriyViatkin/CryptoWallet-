
from sqlalchemy import (Column, Integer,   DateTime,  ForeignKey,  Enum,
                        func, String, Numeric)
from sqlalchemy.orm import relationship
from apps.rest_api_service.src.database import Base
from apps.rest_api_service.enums import OrderStatus

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)

    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    tx_hash = Column(String(66), nullable=True)  # ← null поки оплата не відбулась
    amount = Column(Numeric(38, 18), nullable=False)

    items = relationship("OrderItems", back_populates="order")
    buyer = relationship("User")

