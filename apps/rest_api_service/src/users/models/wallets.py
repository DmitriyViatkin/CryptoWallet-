from sqlalchemy import (Column, Integer, String, DateTime, Enum, ForeignKey,  func,
                        UniqueConstraint)
from sqlalchemy.orm import relationship

from enums import WalletType
from src.database import Base

class Wallet(Base):
    __tablename__ = 'wallets'
    __table_args__ = (
        UniqueConstraint('user_id', 'wallet_address', name='uq_wallet_user_address'),

    )
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    wallet_type = Column( Enum(WalletType), nullable=False)
    private_key_encrypted = Column(String(255), nullable=False)
    wallet_address = Column(String(255),   nullable=False)

    create_at = Column(DateTime, default=func.now())


    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="wallets")
    operations = relationship("WalletOperation", back_populates="wallet")