import pytest
from app.core.database import init_db

@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    """Inicializa o banco de dados antes de todos os testes."""
    init_db()
