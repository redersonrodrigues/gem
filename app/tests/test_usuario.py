from Lib.Escala.Database.criteria import Criteria
from Lib.Escala.Database.repository import Repository
from app.Model.Usuario import Usuario
from Lib.Escala.Database.transaction import Transaction
import sys
import os
# Garante que o diretório raiz do projeto está no sys.path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if root_path not in sys.path:
    sys.path.insert(0, root_path)
# Garante que o diretório 'Lib' está no sys.path
lib_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../../Lib'))
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)
    import pytest


@pytest.fixture(autouse=True)
def transacao():
    try:
        Transaction.close()
    except Exception:
        pass
    Transaction.open("escala")
    yield
    Transaction.close()


def test_criacao_busca_alteracao_delecao_usuario():
    # Criação
    u = Usuario(nome="João Teste", login="joao",
                senha_hash="1234", perfil="admin", status=1)
    u.store()
    assert u.id is not None

    # Busca por id
    u2 = Usuario().load(u.id)
    assert u2 is not None
    assert u2.nome == "João Teste"

    # Alteração
    u2.nome = "João da Silva"
    u2.store()
    u3 = Usuario().load(u2.id)
    assert u3.nome == "João da Silva"

    # Buscar múltiplos (simulação em memória)
    admins = [user for user in Usuario.all() if user.perfil == "admin"]
    assert any(a.id == u3.id for a in admins)

    # Contar
    assert len(admins) >= 1

    # Deletar
    u3.delete()
    assert Usuario().load(u3.id) is None
