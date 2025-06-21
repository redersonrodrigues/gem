import pytest
from sqlalchemy.orm import Session
from app.core.repositories import MedicoRepository, EspecializacaoRepository
from app.models.medico import Medico, StatusMedicoEnum
from app.models.especializacao import Especializacao

@pytest.fixture
def session(db_session):
    # Usa fixture de sessão já existente
    return db_session

def test_medico_validacao_nome_vazio(session):
    repo = MedicoRepository(session)
    esp = Especializacao(nome="Validação")
    session.add(esp)
    session.commit()
    medico = Medico(nome=" ", especializacao_id=esp.id, status=StatusMedicoEnum.ATIVO.value)
    with pytest.raises(ValueError, match="nome do médico é obrigatório"):
        repo.create(medico)

def test_medico_validacao_status_invalido(session):
    repo = MedicoRepository(session)
    esp = Especializacao(nome="Validação")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. Teste", especializacao_id=esp.id, status="desconhecido")
    with pytest.raises(ValueError, match="Status inválido"):
        repo.create(medico)

def test_medico_validacao_especializacao_inexistente(session):
    repo = MedicoRepository(session)
    medico = Medico(nome="Dr. Teste", especializacao_id=9999, status=StatusMedicoEnum.ATIVO.value)
    with pytest.raises(ValueError, match="Especialização não encontrada"):
        repo.create(medico)

def test_especializacao_validacao_nome_vazio(session):
    repo = EspecializacaoRepository(session)
    especializacao = Especializacao(nome=" ")
    with pytest.raises(ValueError, match="nome da especialização é obrigatório"):
        repo.create(especializacao)

def test_medico_validacao_sucesso(session):
    repo = MedicoRepository(session)
    esp = Especializacao(nome="Validação OK")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. OK", especializacao_id=esp.id, status=StatusMedicoEnum.ATIVO.value)
    result = repo.create(medico)
    assert result.id is not None
    assert result.nome == "Dr. OK"
    session.delete(medico)
    session.delete(esp)
    session.commit()
