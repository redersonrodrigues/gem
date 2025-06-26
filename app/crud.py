# Operações CRUD para os modelos
from app.core.database import get_session_local
from app.core.repositories import MedicoRepository, EspecializacaoRepository
from app.models.medico import Medico
from app.models.especializacao import Especializacao

# CRUD para Medico


def create_medico(nome, nome_pj=None, especializacao_id=None, status=None, user_id=None):
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        medico = Medico(
            nome=nome,
            nome_pj=nome_pj,
            especializacao_id=especializacao_id,
            status=status
        )
        return repo.create(medico, user_id)


def get_medicos():
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        return repo.get_all()


def update_medico(
    medico_id, nome=None, nome_pj=None, especializacao_id=None, status=None, user_id=None
):
    SessionLocal = get_session_local()
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
            return repo.update(medico, user_id)
        return None


def delete_medico(medico_id, user_id=None):
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = MedicoRepository(db)
        medico = repo.get_by_id(medico_id)
        if medico and user_id:
            repo.delete(medico, user_id)

# CRUD para Especializacao


def create_especializacao(nome, user_id):
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = Especializacao(nome=nome)
        return repo.create(especializacao, user_id)


def get_especializacoes():
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        return repo.get_all()


def update_especializacao(especializacao_id, nome=None, user_id=None):
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = repo.get_by_id(especializacao_id)
        if especializacao and nome and user_id:
            especializacao.nome = nome
            return repo.update(especializacao, user_id)
        return None


def delete_especializacao(especializacao_id, user_id=None):
    SessionLocal = get_session_local()
    with SessionLocal() as db:
        repo = EspecializacaoRepository(db)
        especializacao = repo.get_by_id(especializacao_id)
        if especializacao and user_id:
            repo.delete(especializacao, user_id)
