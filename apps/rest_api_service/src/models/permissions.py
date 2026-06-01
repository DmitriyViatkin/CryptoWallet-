from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Numeric, \
    Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from apps.rest_api_service.src.database import Base

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    has_chat_access = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="permissions")