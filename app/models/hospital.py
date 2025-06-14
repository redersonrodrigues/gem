from app.models.base import Base
from sqlalchemy import Column, Integer, String


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
