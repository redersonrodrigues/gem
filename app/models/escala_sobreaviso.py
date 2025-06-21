from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class EscalaSobreaviso(Base):
    """
    Modelo ORM para escalas de sobreaviso.

    Cada registro representa um período de sobreaviso para um médico e uma especialização.
    - data_inicial: início do sobreaviso
    - data_final: fim do sobreaviso
    - médico responsável (FK)
    - especialização (FK)
    """
    __tablename__ = 'escalas_sobreaviso'
    id = Column(Integer, primary_key=True)
    data_inicial = Column(Date, nullable=False)  # Data inicial do sobreaviso
    data_final = Column(Date, nullable=False)    # Data final do sobreaviso
    medico1_id = Column(Integer, ForeignKey('medicos.id'), nullable=False)  # FK médico
    especializacao_id = Column(Integer, ForeignKey('especializacoes.id'), nullable=False)  # FK especialização

    medico1 = relationship('app.models.medico.Medico')  # Relação ORM médico
    especializacao = relationship('app.models.especializacao.Especializacao')  # Relação ORM especialização

    def __repr__(self):
        """
        Retorna uma representação legível da escala de sobreaviso para debug/log.
        """
        return (
            f"<EscalaSobreaviso(data_inicial={self.data_inicial}, "
            f"data_final={self.data_final})>"
        )
