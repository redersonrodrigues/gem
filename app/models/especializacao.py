from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Especializacao(Base):
    """
    Modelo ORM para especializações médicas.

    Representa uma especialização disponível para médicos.
    - nome: nome da especialização (único)
    - Relaciona-se com médicos (um para muitos)
    """
    __tablename__ = 'especializacoes'
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True, nullable=False)  # Nome da especialização

    medicos = relationship('Medico', back_populates='especializacao')  # Médicos desta especialização

    def __repr__(self):
        """
        Retorna uma representação legível da especialização para debug/log.
        """
        return f"<Especializacao(nome={self.nome})>"
