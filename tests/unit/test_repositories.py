import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models import Medico, Especializacao
from app.core.repositories import MedicoRepository, EspecializacaoRepository

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def test_especializacao_crud(session):
    repo = EspecializacaoRepository(session)
    esp = Especializacao(nome="Teste Especialização")
    repo.create(esp)
    all_esps = repo.get_all()
    assert any(e.nome == "Teste Especialização" for e in all_esps)
    session.delete(esp)
    session.commit()

def test_medico_crud(session):
    esp = Especializacao(nome="Esp CRUD")
    session.add(esp)
    session.commit()
    repo = MedicoRepository(session)
    medico = Medico(nome="Teste Médico", especializacao_id=esp.id)
    repo.create(medico)
    all_med = repo.get_all()
    assert any(m.nome == "Teste Médico" for m in all_med)
    session.delete(medico)
    session.delete(esp)
    session.commit()

def test_especializacao_crud_erro(session):
    repo = EspecializacaoRepository(session)
    esp = Especializacao(nome=None)  # nome é obrigatório
    with pytest.raises(ValueError):
        repo.create(esp)
    session.rollback()

def test_medico_crud_erro_campos_obrigatorios(session):
    repo = MedicoRepository(session)
    medico = Medico(nome=None, especializacao_id=None)
    with pytest.raises(ValueError):
        repo.create(medico)
    session.rollback()

def test_medico_crud_erro_especialidade_inexistente(session):
    repo = MedicoRepository(session)
    medico = Medico(nome="C", especializacao_id=9999)
    with pytest.raises(ValueError):
        repo.create(medico)
    session.rollback()

def test_update_delete_invalid(session):
    repo_esp = EspecializacaoRepository(session)
    repo_med = MedicoRepository(session)
    esp = Especializacao(nome="Esp Upd")
    repo_esp.create(esp)
    medico = Medico(nome="Med Upd", especializacao_id=esp.id)
    repo_med.create(medico)
    # Update inválido
    medico.nome = None
    with pytest.raises(ValueError):
        repo_med.update(medico)
    # Delete de objeto não persistido
    fake_esp = Especializacao(nome="Fake")
    with pytest.raises(Exception):
        repo_esp.delete(fake_esp)
    session.delete(medico)
    session.delete(esp)
    session.commit()
