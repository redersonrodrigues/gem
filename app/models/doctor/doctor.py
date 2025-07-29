from app.models.base import Base
from sqlalchemy import Column, Integer, String

class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    crm = Column(String, unique=True, nullable=False)
    especialidade = Column(String, nullable=True)
    ativo = Column(Integer, default=1)