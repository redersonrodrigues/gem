import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.core.relatorio_cobertura_minima import relatorio_cobertura_minima, exportar_cobertura_minima_csv
from datetime import date

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def test_relatorio_cobertura_minima_lacuna(session):
    esp = Especializacao(nome="Pediatria")
    session.add(esp)
    session.commit()
    # Nenhum plantão cadastrado
    lacunas = relatorio_cobertura_minima(session, date(2025, 6, 20), date(2025, 6, 21), minimo_por_turno=1)
    assert len(lacunas) == 4  # 2 dias x 2 turnos
    assert lacunas[0][1] == "Pediatria"

def test_relatorio_cobertura_minima_com_plantao(session):
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. Plantão", especializacao_id=esp.id)
    session.add(medico)
    session.commit()
    plantao = EscalaPlantonista(data=date(2025, 6, 20), turno="diurno", medico1_id=medico.id)
    session.add(plantao)
    session.commit()
    lacunas = relatorio_cobertura_minima(session, date(2025, 6, 20), date(2025, 6, 20), minimo_por_turno=1)
    assert len(lacunas) == 1  # Só o turno noturno sem cobertura
    assert lacunas[0][3] == "noturno"

def test_exportar_cobertura_minima_csv(session):
    esp = Especializacao(nome="Ortopedia")
    session.add(esp)
    session.commit()
    lacunas = relatorio_cobertura_minima(session, date(2025, 6, 20), date(2025, 6, 20), minimo_por_turno=1)
    csv_str = exportar_cobertura_minima_csv(lacunas)
    assert "Especialização" in csv_str
    assert "Ortopedia" in csv_str
