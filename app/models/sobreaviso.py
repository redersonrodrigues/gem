from app.models.base import Base
from sqlalchemy import Column, Integer, Date, String, ForeignKey, Index
from sqlalchemy.orm import relationship


class Sobreaviso(Base):
    __tablename__ = "sobreavisos"
    id = Column(Integer, primary_key=True)
    data = Column(Date, nullable=False)
    especialidade = Column(String, nullable=False)
    medico_id = Column(Integer, ForeignKey("doctors.id"), nullable=False, index=True)

    medico = relationship("Doctor", foreign_keys=[medico_id])

    __table_args__ = (
        Index('ix_sobreavisos_data', 'data'),
        Index('ix_sobreavisos_medico_id', 'medico_id'),  # Índice adicionado para medico_id
    )
