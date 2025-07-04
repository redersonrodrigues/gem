import pytest
from app.Service.gerenciador_escalas import GerenciadorEscalas
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_plantonista import EscalaPlantonista

@pytest.fixture(autouse=True)
def transacao():
    from Lib.Escala.Database.transaction import Transaction
    Transaction.open("escala")
    yield
    Transaction.close()

def test_criar_e_buscar_escala_plantonista():
    # Limpa escalas duplicadas antes do teste
    repo = Repository(EscalaPlantonista)
    c = Criteria()
    c.add("data", "=", "2025-07-10")
    c.add("turno", "=", "diurno")
    c.add("medico_0_id", "=", 1)
    c.add("medico_1_id", "=", 2)
    repo.delete(c)

    ger = GerenciadorEscalas("plantonista")
    escala = ger.criar_escala(data="2025-07-10", turno="diurno", medico_0_id=1, medico_1_id=2)
    assert escala.id is not None

    escalas = ger.buscar_escala(data="2025-07-10")
    assert any(e.id == escala.id for e in escalas)