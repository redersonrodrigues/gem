"""
Modelo Log para registro de operações críticas no sistema.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    action = Column(String(64), nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Log(id={self.id}, user_id={self.user_id}, action='{self.action}', timestamp={self.timestamp})>"
