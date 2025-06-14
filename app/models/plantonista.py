from app.models.base import Base
from sqlalchemy import Column, Integer, Date, ForeignKey, Index
from sqlalchemy.orm import relationship


class Plantonista(Base):
    __tablename__ = "plantonistas"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False, index=True)
    diurno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    diurno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    noturno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)
    noturno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)

    diurno_medico1 = relationship("Doctor", foreign_keys=[diurno_medico1_id])
    diurno_medico2 = relationship("Doctor", foreign_keys=[diurno_medico2_id])
    noturno_medico1 = relationship("Doctor", foreign_keys=[noturno_medico1_id])
    noturno_medico2 = relationship("Doctor", foreign_keys=[noturno_medico2_id])

    __table_args__ = (
        Index('ix_plantonistas_data', 'data'),
    )

# Otimização: Adicionados índices nos campos de chave estrangeira e no campo 'data' para melhorar performance de consultas
