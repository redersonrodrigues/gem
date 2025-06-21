import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.core.relatorio_distribuicao_plantoes import RelatorioDistribuicaoPlantoes
from datetime import date
import os

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def criar_medicos(session):
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()
    m1 = Medico(nome="Dr. A", especializacao_id=esp.id)
    m2 = Medico(nome="Dr. B", especializacao_id=esp.id)
    m3 = Medico(nome="Dr. C", especializacao_id=esp.id)
    session.add_all([m1, m2, m3])
    session.commit()
    return [m1, m2, m3]

def test_relatorio_distribuicao_basico(session):
    medicos = criar_medicos(session)
    # Dr. A: 2 plantões, Dr. B: 1 plantão, Dr. C: 0
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 12), turno="noturno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="diurno"))
    session.commit()
    relatorio = RelatorioDistribuicaoPlantoes(session)
    resultado = relatorio.gerar_relatorio(date(2024, 6, 1), date(2024, 6, 30))
    assert resultado[0]['nome'] == "Dr. B"
    assert resultado[0]['quantidade_plantoes'] == 1
    assert resultado[1]['nome'] == "Dr. A"
    assert resultado[1]['quantidade_plantoes'] == 2

def test_relatorio_distribuicao_csv(tmp_path, session):
    medicos = criar_medicos(session)
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 6, 15), turno="diurno"))
    session.commit()
    relatorio = RelatorioDistribuicaoPlantoes(session)
    file_path = tmp_path / "distribuicao.csv"
    relatorio.exportar_csv(date(2024, 6, 1), date(2024, 6, 30), str(file_path))
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    assert "Dr. A" in content and "Dr. B" in content
    assert "quantidade_plantoes" in content

def test_relatorio_distribuicao_pdf(tmp_path, session):
    medicos = criar_medicos(session)
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, data=date(2024, 6, 10), turno="diurno"))
    session.commit()
    relatorio = RelatorioDistribuicaoPlantoes(session)
    file_path = tmp_path / "distribuicao.pdf"
    relatorio.exportar_pdf(date(2024, 6, 1), date(2024, 6, 30), str(file_path))
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 0
