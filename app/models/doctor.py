from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Modelo de médicos
# Aqui ficará a definição da classe Doctor usando SQLAlchemy
class Doctor(Base):
    __tablename__ = 'doctors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization_id = Column(Integer, ForeignKey('specializations.id'))
    specialization = relationship('Specialization')
