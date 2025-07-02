# Modelos de escalas médicas com padrão Strategy
from gem.utils.database import db
from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Padrão Strategy para tipos de escala
class EscalaStrategy(ABC):
    """Classe abstrata para estratégias de escala"""
    
    @abstractmethod
    def calcular_detalhes(self):
        pass


class EscalaPlantonista(EscalaStrategy):
    """Estratégia para escala de plantonista"""
    
    def calcular_detalhes(self):
        return "Detalhes da escala de plantonista"


class EscalaSobreaviso(EscalaStrategy):
    """Estratégia para escala de sobreaviso"""
    
    def calcular_detalhes(self):
        return "Detalhes da escala de sobreaviso"


# Modelos de escala
class Escala(Base):
    """Modelo base para escalas médicas"""
    __tablename__ = 'escala'
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)  # plantonista ou sobreaviso
    medico_id = db.Column(db.Integer, db.ForeignKey(
        'medico.id'), nullable=False)
    medico = db.relationship('Medico', backref='escalas')

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'escala',
        'with_polymorphic': '*'
    }

    def __repr__(self):
        return f'<Escala {self.tipo} - {self.data_inicio} a {self.data_fim}>'


class EscalaPlantonista(Escala):
    """Modelo para escala de plantonista"""
    __tablename__ = 'escala_plantonista'
    id = db.Column(db.Integer, db.ForeignKey('escala.id'), primary_key=True)
    turno = db.Column(db.String(50), nullable=False)  # diurno ou noturno

    __mapper_args__ = {
        'polymorphic_identity': 'plantonista'
    }

    def __repr__(self):
        return f'<EscalaPlantonista {self.turno} - {self.data_inicio}>'


class EscalaSobreaviso(Escala):
    """Modelo para escala de sobreaviso"""
    __tablename__ = 'escala_sobreaviso'
    id = db.Column(db.Integer, db.ForeignKey('escala.id'), primary_key=True)
    especialidade_id = db.Column(db.Integer, db.ForeignKey(
        'especializacao.id'), nullable=False)
    especialidade = db.relationship(
        'Especializacao', backref='escalas_sobreaviso')

    __mapper_args__ = {
        'polymorphic_identity': 'sobreaviso'
    }

    def __repr__(self):
        return f'<EscalaSobreaviso {self.especialidade} - {self.data_inicio}>'