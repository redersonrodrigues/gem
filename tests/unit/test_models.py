"""
Testes unitários para os modelos SQLAlchemy: Medico, Especializacao, EscalaPlantonista, EscalaSobreaviso.
"""
import pytest
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# Importação explícita de todos os modelos para garantir registro único no MetaData
from app.models import medico, especializacao, escala_plantonista, escala_sobreaviso
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def test_especializacao_criacao(session):
    espec = Especializacao(nome="Cardiologia")
    session.add(espec)
    session.commit()
    assert espec.id is not None
    assert espec.nome == "Cardiologia"

def test_medico_criacao(session):
    espec = Especializacao(nome="Ortopedia")
    session.add(espec)
    session.commit()
    medico = Medico(nome="Dr. João", nome_pj="João PJ", especializacao_id=espec.id, status="ativo")
    session.add(medico)
    session.commit()
    assert medico.id is not None
    assert medico.nome == "Dr. João"
    assert medico.status.value == "ativo"
    assert medico.especializacao_id == espec.id

def test_escala_plantonista_criacao(session):
    espec = Especializacao(nome="Pediatria")
    session.add(espec)
    session.commit()
    m1 = Medico(nome="Dr. A", especializacao_id=espec.id, status="ativo")
    m2 = Medico(nome="Dr. B", especializacao_id=espec.id, status="ativo")
    session.add_all([m1, m2])
    session.commit()
    escala = EscalaPlantonista(data=date(2025, 6, 20), turno="diurno", medico1_id=m1.id, medico2_id=m2.id)
    session.add(escala)
    session.commit()
    assert escala.id is not None
    assert escala.turno == "diurno"
    assert escala.medico1_id == m1.id
    assert escala.medico2_id == m2.id

def test_escala_sobreaviso_criacao(session):
    espec = Especializacao(nome="Neurologia")
    session.add(espec)
    session.commit()
    m1 = Medico(nome="Dr. C", especializacao_id=espec.id, status="ativo")
    session.add(m1)
    session.commit()
    escala = EscalaSobreaviso(
        data_inicial=date(2025, 6, 21),
        data_final=date(2025, 6, 22),
        medico1_id=m1.id,
        especializacao_id=espec.id
    )
    session.add(escala)
    session.commit()
    assert escala.id is not None
    assert escala.data_inicial == date(2025, 6, 21)
    assert escala.data_final == date(2025, 6, 22)
    assert escala.medico1_id == m1.id
    assert escala.especializacao_id == espec.id
