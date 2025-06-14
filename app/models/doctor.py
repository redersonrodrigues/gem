from app.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

# Tabela associativa para muitos-para-muitos
doctor_specialization = Table(
    "doctor_specialization",
    Base.metadata,
    Column("doctor_id", Integer, ForeignKey("doctors.id"), primary_key=True),
    Column(
        "specialization_id", Integer, ForeignKey("specializations.id"), primary_key=True
    ),
)


# Modelo de médicos
# Aqui ficará a definição da classe Doctor usando SQLAlchemy
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    fantasy_name = Column(String, nullable=False)  # Nome fantasia PJ
    specializations = relationship(
        "Specialization", secondary=doctor_specialization, back_populates="doctors"
    )
