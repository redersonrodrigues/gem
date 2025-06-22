"""
Teste de conexão com PostgreSQL para validar ambiente de produção.
Necessário: PostgreSQL rodando localmente e variável DATABASE_URL configurada.
"""
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

@pytest.mark.integration
def test_postgres_connection():
    db_url = os.getenv("DATABASE_URL", "postgresql+psycopg2://usuario:senha@localhost:5432/gem")
    engine = create_engine(db_url, echo=False, future=True)
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except OperationalError as e:
        pytest.skip(f"PostgreSQL não disponível ou configuração inválida: {e}")
