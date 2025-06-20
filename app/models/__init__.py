# Modelos de dados (ORM SQLAlchemy)
# Exemplo: Médico, Especialização, Escala, Usuário, etc.

from sqlalchemy import Column, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from .database import Base


class Medico(Base):
    __tablename__ = "medicos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    crm = Column(String, unique=True, index=True)
    especialidade_id = Column(Integer, ForeignKey("especializacoes.id"))

    especialidade = relationship("Especializacao", back_populates="medicos")
    escalas = relationship("Escala", back_populates="medico")


class Especializacao(Base):
    __tablename__ = "especializacoes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)

    medicos = relationship("Medico", back_populates="especialidade")


class Escala(Base):
    __tablename__ = "escalas"

    id = Column(Integer, primary_key=True, index=True)
    medico_id = Column(Integer, ForeignKey("medicos.id"))
    dia_da_semana = Column(String, index=True)
    horario_inicio = Column(Time)
    horario_fim = Column(Time)

    medico = relationship("Medico", back_populates="escalas")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)