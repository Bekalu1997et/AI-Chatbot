from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    role = Column(String)  # "user" or "assistant"
    message = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
