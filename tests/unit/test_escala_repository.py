import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.escala import Escala
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.core.escala_repository import EscalaRepository

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def test_crud_escala(session):
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. Escala", especializacao_id=esp.id)
    session.add(medico)
    session.commit()
    repo = EscalaRepository(session)
    escala = Escala(data="2025-06-22", medico_id=medico.id, especializacao_id=esp.id)
    result = repo.create(escala, user_id=1)
    assert result.id is not None
    assert result.medico_id == medico.id
    # Testa update
    escala.data = "2025-06-23"
    updated = repo.update(escala, user_id=1)
    assert updated.data == "2025-06-23"
    # Testa delete
    repo.delete(escala, user_id=1)
    assert session.query(Escala).count() == 0

def test_escala_validacao_campos_obrigatorios(session):
    repo = EscalaRepository(session)
    escala = Escala(data=None, medico_id=None, especializacao_id=None)
    with pytest.raises(ValueError):
        repo.create(escala, user_id=1)
    session.rollback()
