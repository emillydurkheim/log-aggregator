from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)  # Ex: "auth-service", "payment-api"
    level = Column(String, index=True)         # Ex: "INFO", "WARNING", "ERROR"
    message = Column(Text)                     # A descrição detalhada do erro
    timestamp = Column(DateTime, default=datetime.utcnow)