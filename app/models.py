# Modelos do banco de dados
from .database import db
from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hospital(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)


class Medico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    especializacoes = db.relationship(
        'Especializacao', secondary='medico_especializacao', back_populates='medicos')
    escalas_associadas = db.relationship('Escala', backref='medico_associado')

    def __init__(self, nome):
        self.nome = nome.upper()


class Especializacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    medicos = db.relationship(
        'Medico', secondary='medico_especializacao', back_populates='especializacoes')

    def __init__(self, nome):
        self.nome = nome.upper()


# Tabela de associação para muitos-para-muitos entre Medico e Especializacao
medico_especializacao = db.Table('medico_especializacao',
                                 db.Column('medico_id', db.Integer, db.ForeignKey(
                                     'medico.id'), primary_key=True),
                                 db.Column('especializacao_id', db.Integer, db.ForeignKey(
                                     'especializacao.id'), primary_key=True)
                                 )


# Normalização e ajustes nos relacionamentos
class EscalaStrategy(ABC):
    @abstractmethod
    def calcular_detalhes(self):
        pass


class EscalaPlantonista(EscalaStrategy):
    def calcular_detalhes(self):
        return "Detalhes da escala de plantonista"


class EscalaSobreaviso(EscalaStrategy):
    def calcular_detalhes(self):
        return "Detalhes da escala de sobreaviso"


class Escala(Base):
    __tablename__ = 'escala'
    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    # plantonista ou sobreaviso
    tipo = db.Column(db.String(50), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey(
        'medico.id'), nullable=False)
    medico = db.relationship('Medico', backref='escalas')

    __mapper_args__ = {
        'polymorphic_on': tipo,
        'polymorphic_identity': 'escala',
        'with_polymorphic': '*'
    }


class EscalaPlantonista(Escala):
    __tablename__ = 'escala_plantonista'
    id = db.Column(db.Integer, db.ForeignKey('escala.id'), primary_key=True)
    turno = db.Column(db.String(50), nullable=False)  # diurno ou noturno

    __mapper_args__ = {
        'polymorphic_identity': 'plantonista'
    }


class EscalaSobreaviso(Escala):
    __tablename__ = 'escala_sobreaviso'
    id = db.Column(db.Integer, db.ForeignKey('escala.id'), primary_key=True)
    especialidade_id = db.Column(db.Integer, db.ForeignKey(
        'especializacao.id'), nullable=False)
    especialidade = db.relationship(
        'Especializacao', backref='escalas_sobreaviso')

    __mapper_args__ = {
        'polymorphic_identity': 'sobreaviso'
    }


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(100), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.String(100), nullable=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
