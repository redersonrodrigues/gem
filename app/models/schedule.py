from app.models.base import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Time

# Modelo de escalas
# Aqui ficará a definição da classe Schedule usando SQLAlchemy


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False, unique=True)
    # Plantonistas
    diurno_medico1_id = Column(Integer, ForeignKey("doctors.id"))
    diurno_medico2_id = Column(Integer, ForeignKey("doctors.id"))
    noturno_medico1_id = Column(Integer, ForeignKey("doctors.id"))
    noturno_medico2_id = Column(Integer, ForeignKey("doctors.id"))
    # Sobreaviso ortopedia (quinzenal)
    ortopedia_medico_id = Column(Integer, ForeignKey("doctors.id"))
    # Sobreaviso demais especialidades (semanal)
    sobreaviso_especialidade = Column(String)  # Nome da especialidade
    sobreaviso_medico_id = Column(Integer, ForeignKey("doctors.id"))
    # Tipo de escala (PLANTONISTA, SOBREAVISO_ORTOPEDIA, SOBREAVISO_OUTRAS)
    tipo = Column(String, nullable=False)
