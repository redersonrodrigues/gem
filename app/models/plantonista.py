from app.models.base import Base
from sqlalchemy import Column, Integer, Date, ForeignKey

class Plantonista(Base):
    __tablename__ = "plantonistas"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    diurno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    diurno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    noturno_medico1_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    noturno_medico2_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)