import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.core.relatorio_medicos_por_especializacao import listar_medicos_por_especializacao, exportar_medicos_por_especializacao_csv, exportar_medicos_por_especializacao_pdf
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
    esp1 = Especializacao(nome="Cardiologia")
    esp2 = Especializacao(nome="Ortopedia")
    session.add_all([esp1, esp2])
    session.commit()
    m1 = Medico(nome="Dr. A", especializacao_id=esp1.id, nome_pj="PJ A", status="ativo")
    m2 = Medico(nome="Dr. B", especializacao_id=esp1.id, nome_pj="PJ B", status="inativo")
    m3 = Medico(nome="Dr. C", especializacao_id=esp2.id, nome_pj="PJ C", status="ativo")
    session.add_all([m1, m2, m3])
    session.commit()
    return [m1, m2, m3]

def test_listar_medicos_por_especializacao(session):
    criar_medicos(session)
    dados = listar_medicos_por_especializacao(session)
    assert any(d["especializacao"] == "Cardiologia" for d in dados)
    assert any(d["especializacao"] == "Ortopedia" for d in dados)
    assert any(d["medico"] == "Dr. A" for d in dados)
    assert any(d["status"] == "ativo" for d in dados)

def test_exportar_medicos_por_especializacao_csv(tmp_path, session):
    criar_medicos(session)
    dados = listar_medicos_por_especializacao(session)
    file_path = tmp_path / "medicos_especializacao.csv"
    exportar_medicos_por_especializacao_csv(dados, str(file_path))
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    assert "Cardiologia" in content and "Ortopedia" in content
    assert "Dr. A" in content and "Dr. C" in content

def test_exportar_medicos_por_especializacao_pdf(tmp_path, session):
    criar_medicos(session)
    dados = listar_medicos_por_especializacao(session)
    file_path = tmp_path / "medicos_especializacao.pdf"
    exportar_medicos_por_especializacao_pdf(dados, str(file_path))
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 0
