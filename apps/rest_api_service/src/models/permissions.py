from sqlalchemy import Column, Integer,  ForeignKey, Boolean
from sqlalchemy.orm import relationship
from  src.database import Base

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True, index=True)
    has_chat_access = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="permissions")