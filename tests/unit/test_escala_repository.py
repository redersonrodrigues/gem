import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.escala_plantonista import EscalaPlantonista
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

def test_crud_escala_plantonista(session):
    medico1 = Medico(nome="Dr. Plantonista 1")
    medico2 = Medico(nome="Dr. Plantonista 2")
    session.add_all([medico1, medico2])
    session.commit()
    repo = EscalaRepository(session)
    escala = EscalaPlantonista(data="2025-06-22", turno="diurno", medico1_id=medico1.id, medico2_id=medico2.id)
    result = repo.create(escala, user_id=1)
    assert result.id is not None
    assert result.medico1_id == medico1.id
    # Testa update
    escala.data = "2025-06-23"
    updated = repo.update(escala, user_id=1)
    assert str(updated.data) == "2025-06-23"
    # Testa delete
    repo.delete(escala, user_id=1)
    assert session.query(EscalaPlantonista).count() == 0

def test_escala_plantonista_validacao_campos_obrigatorios(session):
    repo = EscalaRepository(session)
    escala = EscalaPlantonista(data=None, turno=None, medico1_id=None)
    with pytest.raises(ValueError):
        repo.create(escala, user_id=1)
    session.rollback()
