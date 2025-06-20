from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Especializacao(Base):
    __tablename__ = 'especializacoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)

    medicos = relationship('Medico', back_populates='especializacao')

    def __repr__(self):
        return f"<Especializacao(nome={self.nome})>"
