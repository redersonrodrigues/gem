from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Medico(Base):
    """
    Modelo ORM para médicos.

    Representa um médico do hospital, incluindo:
    - nome completo
    - nome da pessoa jurídica (opcional)
    - especialização (chave estrangeira para Especializacao)
    - status de atividade ('ativo' ou 'inativo')
    """
    __tablename__ = 'medicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)  # Nome completo do médico
    nome_pj = Column(String)  # Nome da pessoa jurídica (opcional)
    especializacao_id = Column(
        Integer, ForeignKey('especializacoes.id'), nullable=False
    )  # FK para especialização
    status = Column(
        String, nullable=False, default='ativo'
    )  # Status do médico: 'ativo' ou 'inativo'

    especializacao = relationship('Especializacao', back_populates='medicos')  # Relação ORM

    def __repr__(self):
        """
        Retorna uma representação legível do médico para debug/log.
        """
        return f"<Medico(nome={self.nome}, status={self.status})>"
