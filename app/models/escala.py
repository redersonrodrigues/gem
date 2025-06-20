from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Escala(Base):
    __tablename__ = 'escalas'
    id = Column(Integer, primary_key=True)
    tipo = Column(String, nullable=False)  # plantonista ou sobreaviso
    data = Column(Date, nullable=True)  # para plantonista
    data_inicial = Column(Date, nullable=True)  # para sobreaviso
    data_final = Column(Date, nullable=True)  # para sobreaviso
    turno = Column(String, nullable=True)  # diurno, noturno (plantonista)
    medico1_id = Column(Integer, ForeignKey('medicos.id'))
    medico2_id = Column(Integer, ForeignKey('medicos.id'), nullable=True)
    especializacao_id = Column(Integer, ForeignKey('especializacoes.id'), nullable=True)

    medico1 = relationship('Medico', foreign_keys=[medico1_id])
    medico2 = relationship('Medico', foreign_keys=[medico2_id])
    especializacao = relationship('Especializacao')

    def __repr__(self):
        return f"<Escala(tipo={self.tipo}, data={self.data}, turno={self.turno})>"
