import subprocess
import os
import tempfile
import pytest
from app.core.database import get_session_local
from app.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão de banco de dados isolada para cada teste unitário.
    Usa um arquivo SQLite temporário para garantir isolamento e persistência do schema.
    Aplica as migrations Alembic no banco temporário antes de iniciar a sessão.
    """
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_url = f"sqlite:///{tmpfile.name}"
    # Define a variável de ambiente para o Alembic usar o banco correto
    os.environ["DATABASE_URL"] = db_url
    # Executa as migrations Alembic no banco temporário
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    # Cria engine e sessão para o banco temporário
    engine = create_engine(db_url)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()
        engine.dispose()
        os.unlink(tmpfile.name)
