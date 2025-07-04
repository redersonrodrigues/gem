import pytest
from Lib.Escala.Database.transaction import Transaction
from app.Model.especializacao import Especializacao
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria

@pytest.fixture(autouse=True)
def transacao():
    Transaction.open("escala")
    yield
    Transaction.close()

def test_repository_criteria_especializacao():
    # Criação de especializações
    e1 = Especializacao(nome="Cardiologia")
    e1.store()
    e2 = Especializacao(nome="Neurologia")
    e2.store()

    # Busca por nome
    c = Criteria()
    c.add("nome", "=", "Cardiologia")
    repo = Repository(Especializacao)
    cardiologistas = repo.load(c)

    assert any(e.id == e1.id for e in cardiologistas)
    assert all(e.nome == "Cardiologia" for e in cardiologistas)

    # Busca por todos
    todas = repo.load()
    assert len(todas) >= 2

    # Deletar para limpar dados de teste
    e1.delete()
    e2.delete()