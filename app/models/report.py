from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
import datetime


class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    type = Column(String, nullable=False)  # Ex: 'plantonista', 'sobreaviso', 'custom'
    filters = Column(Text)  # JSON string com filtros aplicados
