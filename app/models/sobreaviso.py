from app.models.base import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey

class Sobreaviso(Base):
    __tablename__ = "sobreavisos"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    especialidade = Column(String, nullable=False)
    medico_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)