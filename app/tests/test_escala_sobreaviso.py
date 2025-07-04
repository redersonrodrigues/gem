import pytest
from app.Service.gerenciador_escalas import GerenciadorEscalas
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_sobreaviso import EscalaSobreaviso

@pytest.fixture(autouse=True)
def transacao():
    from Lib.Escala.Database.transaction import Transaction
    Transaction.open("escala")
    yield
    Transaction.close()

def test_criar_e_buscar_escala_sobreaviso():
    # Limpa escalas duplicadas antes do teste
    repo = Repository(EscalaSobreaviso)
    c = Criteria()
    c.add("data_inicial", "=", "2025-07-10")
    c.add("data_final", "=", "2025-07-12")
    c.add("medico_id", "=", 1)
    c.add("especializacao_id", "=", 1)
    repo.delete(c)

    ger = GerenciadorEscalas("sobreaviso")
    escala = ger.criar_escala(data_inicial="2025-07-10", data_final="2025-07-12", medico_id=1, especializacao_id=1)
    assert escala.id is not None

    escalas = ger.buscar_escala(data="2025-07-11")
    assert any(e.id == escala.id for e in escalas)