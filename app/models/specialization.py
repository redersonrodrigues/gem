from sqlalchemy import Column, Integer, String

from .database import Base


# Modelo de especializações médicas
# Aqui ficará a definição da classe Specialization usando SQLAlchemy
class Specialization(Base):
    __tablename__ = "specializations"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
