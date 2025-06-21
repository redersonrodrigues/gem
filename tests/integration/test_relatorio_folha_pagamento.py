import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.escala_plantonista import EscalaPlantonista
from app.models.escala_sobreaviso import EscalaSobreaviso
from app.core.relatorio_folha_pagamento import consultar_escalas_folha_pagamento, exportar_folha_pagamento_csv, exportar_folha_pagamento_pdf
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

def criar_dados(session):
    esp = Especializacao(nome="Clínica Geral")
    session.add(esp)
    session.commit()
    m1 = Medico(nome="Dr. A", especializacao_id=esp.id, nome_pj="PJ A")
    m2 = Medico(nome="Dr. B", especializacao_id=esp.id, nome_pj="PJ B")
    session.add_all([m1, m2])
    session.commit()
    p1 = EscalaPlantonista(medico1_id=m1.id, data=date(2025, 6, 20), turno="diurno")
    s1 = EscalaSobreaviso(medico1_id=m2.id, especializacao_id=esp.id, data_inicial=date(2025, 6, 21), data_final=date(2025, 6, 21))
    session.add_all([p1, s1])
    session.commit()
    return m1, m2

def test_consultar_escalas_folha_pagamento(session):
    criar_dados(session)
    dados = consultar_escalas_folha_pagamento(session, date(2025, 6, 19), date(2025, 6, 22))
    assert any(d["tipo"] == "Plantão" for d in dados)
    assert any(d["tipo"] == "Sobreaviso" for d in dados)
    assert any(d["nome_pj"] == "PJ A" for d in dados)
    assert any(d["nome_pj"] == "PJ B" for d in dados)

def test_exportar_folha_pagamento_csv(tmp_path, session):
    criar_dados(session)
    dados = consultar_escalas_folha_pagamento(session, date(2025, 6, 19), date(2025, 6, 22))
    file_path = tmp_path / "folha.csv"
    exportar_folha_pagamento_csv(dados, str(file_path))
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    assert "Plantão" in content and "Sobreaviso" in content
    assert "nome_pj" in content

def test_exportar_folha_pagamento_pdf(tmp_path, session):
    criar_dados(session)
    dados = consultar_escalas_folha_pagamento(session, date(2025, 6, 19), date(2025, 6, 22))
    file_path = tmp_path / "folha.pdf"
    exportar_folha_pagamento_pdf(dados, str(file_path))
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) > 0
