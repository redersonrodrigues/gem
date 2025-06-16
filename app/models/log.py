from app.models.base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    entity = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=True)
    timestamp = Column(
        DateTime, default=lambda: datetime.datetime.now(datetime.UTC))
    user = relationship("User", back_populates="logs")
