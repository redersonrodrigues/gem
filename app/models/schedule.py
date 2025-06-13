from app.models.base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

# Modelo de escalas
# Aqui ficará a definição da classe Schedule usando SQLAlchemy

class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    data = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    medico1_id = Column(Integer, ForeignKey('doctors.id'))
    medico2_id = Column(Integer, ForeignKey('doctors.id'))
