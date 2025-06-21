from sqlalchemy import Column, Integer, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base


class EscalaPlantonista(Base):
    """
    Modelo ORM para escalas de plantonistas.

    Cada registro representa um plantão diário, com:
    - data do plantão
    - turno ('diurno' ou 'noturno')
    - dois médicos (referências para Medico)
    """
    __tablename__ = 'escalas_plantonistas'
    __table_args__ = (
        UniqueConstraint('data', 'turno', name='uix_data_turno'),
    )
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)  # Data do plantão
    turno = Column(String, nullable=False)  # Turno: 'diurno' ou 'noturno'
    medico1_id = Column(
        Integer, ForeignKey('medicos.id'), nullable=False
    )  # FK médico 1
    medico2_id = Column(
        Integer, ForeignKey('medicos.id'), nullable=True
    )  # FK médico 2 (opcional)

    medico1 = relationship(
        'app.models.medico.Medico', foreign_keys=[medico1_id], back_populates='escalas_plantonista1'
    )  # Relação ORM médico 1
    medico2 = relationship(
        'app.models.medico.Medico', foreign_keys=[medico2_id], back_populates='escalas_plantonista2'
    )  # Relação ORM médico 2
    version = Column(Integer, nullable=False, default=1)
    __mapper_args__ = {"version_id_col": version}

    def __repr__(self):
        """
        Retorna uma representação legível da escala de plantonista para
        debug/log.
        """
        return f"<EscalaPlantonista(data={self.data}, turno={self.turno})>"

    def duracao_horas(self):
        """
        Retorna a duração do plantão em horas.
        Por padrão, considera 12h para cada plantão (diurno ou noturno).
        """
        return 12
