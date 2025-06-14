from app.models.base import Base
from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class Plantonista(Base):
    __tablename__ = "plantonistas"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    diurno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    diurno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    noturno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    noturno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    diurno_medico1 = relationship("Doctor", foreign_keys=[diurno_medico1_id])
    diurno_medico2 = relationship("Doctor", foreign_keys=[diurno_medico2_id])
    noturno_medico1 = relationship("Doctor", foreign_keys=[noturno_medico1_id])
    noturno_medico2 = relationship("Doctor", foreign_keys=[noturno_medico2_id])
