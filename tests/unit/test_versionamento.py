"""
Testes para versionamento de dados e histórico de alterações.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.models.medico import Medico, StatusMedicoEnum
from app.models.especializacao import Especializacao
from app.models.historico_versao import HistoricoVersao
from app.models import audit_listener  # Garante registro dos listeners
import os

@pytest.fixture
def session_temp():
    engine = create_engine('sqlite:///:memory:', echo=False, future=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_versionamento_medico(session_temp):
    especializacao = Especializacao(nome="Cardiologia")
    session_temp.add(especializacao)
    session_temp.commit()
    medico = Medico(nome="Dr. Teste", especializacao_id=especializacao.id, status=StatusMedicoEnum.ATIVO.value)
    session_temp.add(medico)
    session_temp.commit()
    # Atualiza médico
    medico.nome = "Dr. Teste 2"
    session_temp.commit()
    # Consulta histórico
    historicos = session_temp.query(HistoricoVersao).filter_by(tabela="medicos", registro_id=medico.id).all()
    assert len(historicos) >= 1
    assert any("Dr. Teste" in h.dados or "Dr. Teste 2" in h.dados for h in historicos)
