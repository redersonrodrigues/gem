# Operações CRUD para os modelos
from app.core.database import SessionLocal
from app.core.repositories import MedicoRepository, EspecializacaoRepository
from app.models.medico import Medico
from app.models.especializacao import Especializacao

# CRUD para Medico


def create_medico(nome, nome_pj=None, especializacao_id=None, status=None):
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        medico = Medico(
            nome=nome,
            nome_pj=nome_pj,
            especializacao_id=especializacao_id,
            status=status
        )
        return repo.create(medico)


def get_medicos():
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        return repo.get_all()


def update_medico(
    medico_id, nome=None, nome_pj=None, especializacao_id=None, status=None
):
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        medico = repo.get_by_id(medico_id)
        if medico:
            if nome:
                medico.nome = nome
            if nome_pj:
                medico.nome_pj = nome_pj
            if especializacao_id:
                medico.especializacao_id = especializacao_id
            if status:
                medico.status = status
            return repo.update(medico)
        return None


def delete_medico(medico_id):
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        medico = repo.get_by_id(medico_id)
        if medico:
            repo.delete(medico)

# CRUD para Especializacao


def create_especializacao(nome):
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = Especializacao(nome=nome)
        return repo.create(especializacao)


def get_especializacoes():
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        return repo.get_all()


def update_especializacao(especializacao_id, nome=None):
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = repo.get_by_id(especializacao_id)
        if especializacao and nome:
            especializacao.nome = nome
            return repo.update(especializacao)
        return None


def delete_especializacao(especializacao_id):
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = repo.get_by_id(especializacao_id)
        if especializacao:
            repo.delete(especializacao)
