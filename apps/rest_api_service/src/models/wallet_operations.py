from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Numeric, \
    Enum, func
from sqlalchemy.orm import relationship

from apps.rest_api_service.src.database import Base
from apps.rest_api_service.enums import OperationType, StatusPayment


class WalletOperation(Base):
    __tablename__ = 'wallet_operations'

    id = Column(Integer, primary_key=True, index=True)


    tx_hash = Column(String(66), unique=True, index=True, nullable=False)

    from_address = Column(String(42), index=True, nullable=False)
    to_address = Column(String(42), index=True, nullable=False)


    amount = Column(Numeric(38, 18), nullable=False)

    operation_type = Column(Enum(OperationType), nullable=False)


    status = Column(Enum(StatusPayment), default="PENDING", nullable=False)


    block_number = Column(Integer, nullable=True)


    create_at = Column(DateTime, default=func.now())


    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    wallet = relationship("Wallet", back_populates="operations")