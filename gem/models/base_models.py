# Modelos de dados do sistema
from gem.utils.database import db
from abc import ABC, abstractmethod
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tabela de associação para muitos-para-muitos entre Medico e Especializacao
medico_especializacao = db.Table('medico_especializacao',
                                 db.Column('medico_id', db.Integer, db.ForeignKey(
                                     'medico.id'), primary_key=True),
                                 db.Column('especializacao_id', db.Integer, db.ForeignKey(
                                     'especializacao.id'), primary_key=True)
                                 )


class Hospital(db.Model):
    """Modelo para representar um hospital"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Hospital {self.nome}>'


class Medico(db.Model):
    """Modelo para representar um médico"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    especializacoes = db.relationship(
        'Especializacao', secondary='medico_especializacao', back_populates='medicos')
    escalas_associadas = db.relationship('Escala', backref='medico_associado')

    def __init__(self, nome):
        self.nome = nome.upper()

    def __repr__(self):
        return f'<Medico {self.nome}>'


class Especializacao(db.Model):
    """Modelo para representar uma especialização médica"""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    medicos = db.relationship(
        'Medico', secondary='medico_especializacao', back_populates='especializacoes')

    def __init__(self, nome):
        self.nome = nome.upper()

    def __repr__(self):
        return f'<Especializacao {self.nome}>'


class User(db.Model):
    """Modelo para representar um usuário do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


class Log(db.Model):
    """Modelo para registrar logs do sistema"""
    id = db.Column(db.Integer, primary_key=True)
    acao = db.Column(db.String(100), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    usuario = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Log {self.acao} - {self.usuario}>'