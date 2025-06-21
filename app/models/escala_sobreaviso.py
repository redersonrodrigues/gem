from sqlalchemy import Column, Integer, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class EscalaSobreaviso(Base):
    """
    Modelo ORM para escalas de sobreaviso.

    Cada registro representa um período de sobreaviso para um médico e uma
    especialização.
    - data_inicial: início do sobreaviso
    - data_final: fim do sobreaviso
    - médico responsável (FK)
    - especialização (FK)
    """
    __tablename__ = 'escalas_sobreaviso'
    __table_args__ = (
        UniqueConstraint('data_inicial', 'data_final', 'medico1_id', 'especializacao_id', name='uix_sobreaviso_periodo_medico_especializacao'),
    )
    id = Column(Integer, primary_key=True)
    data_inicial = Column(Date, nullable=False)  # Data inicial do sobreaviso
    data_final = Column(Date, nullable=False)    # Data final do sobreaviso
    medico1_id = Column(
        Integer, ForeignKey('medicos.id'), nullable=False
    )  # FK médico
    especializacao_id = Column(
        Integer, ForeignKey('especializacoes.id'), nullable=False
    )  # FK especialização

    medico1 = relationship('app.models.medico.Medico', back_populates='escalas_sobreaviso')  # Relação ORM médico
    especializacao = relationship(
        'app.models.especializacao.Especializacao'
    )  # Relação ORM especialização
    version = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {"version_id_col": version}

    def __repr__(self):
        """
        Retorna uma representação legível da escala de sobreaviso para
        debug/log.
        """
        return (
            f"<EscalaSobreaviso(data_inicial={self.data_inicial}, "
            f"data_final={self.data_final})>"
        )

    def duracao_horas(self):
        """
        Retorna a duração do sobreaviso em horas.
        Por padrão, considera 12h para cada sobreaviso (ajuste conforme regra de negócio).
        """
        return 12
