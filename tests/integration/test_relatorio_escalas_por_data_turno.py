import pytest
from datetime import date
from sqlalchemy.orm import Session
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.core.relatorio_escalas_por_data_turno import listar_escalas_por_data_turno, exportar_escalas_por_data_turno_csv, exportar_escalas_por_data_turno_pdf
import os

@pytest.fixture(autouse=True)
def limpar_tabelas(session):
    session.query(EscalaPlantonista).delete()
    session.query(Medico).delete()
    session.query(Especializacao).delete()
    session.commit()

@pytest.fixture
def setup_db(session):
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()
    m1 = Medico(nome="Dr. X", status="ativo", especializacao_id=esp.id)
    m2 = Medico(nome="Dr. Y", status="ativo", especializacao_id=esp.id)
    session.add_all([m1, m2])
    session.commit()
    return esp, [m1, m2]

def test_listar_escalas_por_data_turno(session, setup_db):
    esp, medicos = setup_db
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, medico2_id=medicos[1].id, data=date(2024, 7, 1), turno="diurno"))
    session.add(EscalaPlantonista(medico1_id=medicos[1].id, data=date(2024, 7, 1), turno="noturno"))
    session.commit()
    dados = listar_escalas_por_data_turno(session)
    assert any(d["turno"] == "diurno" and d["medico1"] == "Dr. X" and d["medico2"] == "Dr. Y" for d in dados)
    assert any(d["turno"] == "noturno" and d["medico1"] == "Dr. Y" for d in dados)

def test_exportar_escalas_por_data_turno_csv(tmp_path, session, setup_db):
    esp, medicos = setup_db
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, medico2_id=medicos[1].id, data=date(2024, 7, 1), turno="diurno"))
    session.commit()
    dados = listar_escalas_por_data_turno(session)
    file_path = tmp_path / "escalas_data_turno.csv"
    exportar_escalas_por_data_turno_csv(dados, str(file_path))
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    assert "Dr. X" in content and "Dr. Y" in content

def test_exportar_escalas_por_data_turno_pdf(tmp_path, session, setup_db):
    esp, medicos = setup_db
    session.add(EscalaPlantonista(medico1_id=medicos[0].id, medico2_id=medicos[1].id, data=date(2024, 7, 1), turno="diurno"))
    session.commit()
    dados = listar_escalas_por_data_turno(session)
    file_path = tmp_path / "escalas_data_turno.pdf"
    exportar_escalas_por_data_turno_pdf(dados, str(file_path))
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 0
