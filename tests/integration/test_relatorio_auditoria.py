import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from app.models.audit_log import AuditLog
from app.core.relatorio_auditoria import consultar_auditoria, exportar_auditoria_csv
from datetime import datetime

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()
    Base.metadata.drop_all(engine)

def test_consultar_auditoria_insercao_medico(session):
    esp = Especializacao(nome="Cardiologia")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. Auditoria", especializacao_id=esp.id)
    session.add(medico)
    session.commit()
    auditoria = consultar_auditoria(session, tabela="medicos")
    assert len(auditoria) > 0
    assert auditoria[0]["operacao"] == "INSERT"
    assert auditoria[0]["tabela"] == "medicos"

def test_exportar_auditoria_csv(session):
    esp = Especializacao(nome="Ortopedia")
    session.add(esp)
    session.commit()
    medico = Medico(nome="Dr. CSV", especializacao_id=esp.id)
    session.add(medico)
    session.commit()
    auditoria = consultar_auditoria(session, tabela="medicos")
    csv_str = exportar_auditoria_csv(auditoria)
    assert "usuario" in csv_str
    assert "INSERT" in csv_str
    assert "medicos" in csv_str
