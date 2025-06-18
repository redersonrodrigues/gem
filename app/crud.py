# Operações CRUD para os modelos
from .models import db, Hospital, Medico, Especializacao


def create_hospital(nome, endereco):
    hospital = Hospital(nome=nome, endereco=endereco)
    db.session.add(hospital)
    db.session.commit()
    return hospital


def get_hospitals():
    return Hospital.query.all()


def update_hospital(hospital_id, nome=None, endereco=None):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        if nome:
            hospital.nome = nome
        if endereco:
            hospital.endereco = endereco
        db.session.commit()
    return hospital


def delete_hospital(hospital_id):
    hospital = Hospital.query.get(hospital_id)
    if hospital:
        db.session.delete(hospital)
        db.session.commit()

# CRUD para Medico


def create_medico(nome):
    medico = Medico(nome=nome)
    db.session.add(medico)
    db.session.commit()
    return medico


def get_medicos():
    return Medico.query.all()


def update_medico(medico_id, nome=None):
    medico = Medico.query.get(medico_id)
    if medico and nome:
        medico.nome = nome
        db.session.commit()
    return medico


def delete_medico(medico_id):
    medico = Medico.query.get(medico_id)
    if medico:
        db.session.delete(medico)
        db.session.commit()

# CRUD para Especializacao


def create_especializacao(nome):
    especializacao = Especializacao(nome=nome)
    db.session.add(especializacao)
    db.session.commit()
    return especializacao


def get_especializacoes():
    return Especializacao.query.all()


def update_especializacao(especializacao_id, nome=None):
    especializacao = Especializacao.query.get(especializacao_id)
    if especializacao and nome:
        especializacao.nome = nome
        db.session.commit()
    return especializacao


def delete_especializacao(especializacao_id):
    especializacao = Especializacao.query.get(especializacao_id)
    if especializacao:
        db.session.delete(especializacao)
        db.session.commit()
