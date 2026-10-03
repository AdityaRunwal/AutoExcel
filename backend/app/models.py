from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class CleaningHistory(Base):
    __tablename__ = "cleaning_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    prompt = Column(String)
    operations = Column(String)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)