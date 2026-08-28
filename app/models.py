from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)

    messages = relationship("Message", back_populates="sender")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(String, nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    content = Column(String, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    sender = relationship("User", back_populates="messages")