import sys
import os
# Garante que o diretório raiz do projeto está no sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

import pytest
from Lib.Escala.Database.transaction import Transaction
from app.Model.medico import Medico
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria

@pytest.fixture(autouse=True)
def transacao():
    Transaction.open("escala")
    yield
    Transaction.close()

def test_repository_criteria_medico():
    # Criação de médicos para teste
    m1 = Medico(nome="Dr. Ana", nome_pj="Ana LTDA", especializacao_id=1, status="ativo")
    m1.store()
    m2 = Medico(nome="Dr. Carlos", nome_pj="Carlos ME", especializacao_id=2, status="ativo")
    m2.store()
    m3 = Medico(nome="Dr. Ana", nome_pj="Ana Clínica", especializacao_id=1, status="inativo")
    m3.store()

    # Buscar todos médicos com especializacao_id = 1 e status = 'ativo'
    c = Criteria()
    c.add("especializacao_id", "=", 1)
    c.add("status", "=", "ativo")
    repo = Repository(Medico)
    medicos = repo.load(c)

    assert any(m.id == m1.id for m in medicos)
    assert all(m.especializacao_id == 1 and m.status == "ativo" for m in medicos)

    # Buscar médicos pelo nome
    c2 = Criteria()
    c2.add("nome", "=", "Dr. Ana")
    repo2 = Repository(Medico)
    anas = repo2.load(c2)
    assert len(anas) >= 2
    assert all(m.nome == "Dr. Ana" for m in anas)

    # Contar médicos ativos
    c3 = Criteria()
    c3.add("status", "=", "ativo")
    count = repo.count(c3)
    assert count >= 2

    # Limpar dados de teste
    m1.delete()
    m2.delete()
    m3.delete()