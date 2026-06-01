from sqlalchemy import Column, Integer, String, DateTime,  func, Boolean
from sqlalchemy.orm import relationship
from  src.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50),  nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100))
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    avatar_url = Column(String(255))
    is_active = Column(Boolean, default=True) 

    # Relationships
    permissions = relationship("Permission", back_populates="user", uselist=False)
    wallets = relationship("Wallet", back_populates="user")
    products = relationship("Product", back_populates="user")
    orders = relationship("Order", back_populates="buyer")