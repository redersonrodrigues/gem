from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class Medico(Base):
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    nome_pj = Column(String)
    especializacao_id = Column(Integer, ForeignKey('especializacoes.id'))
    status = Column(Boolean, default=True)

    especializacao = relationship('Especializacao', back_populates='medicos')

    def __repr__(self):
        return f"<Medico(nome={self.nome}, status={'Ativo' if self.status else 'Inativo'})>"
