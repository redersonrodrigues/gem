import sys
import os
# Adiciona o diretório absoluto de gem/ ao sys.path para garantir importação do pacote app
GEM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if GEM_PATH not in sys.path:
    sys.path.insert(0, GEM_PATH)

import subprocess
import tempfile
import pytest
from app.core.database import get_session_local
from app.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(message)s')

@pytest.fixture(scope="function")
def db_session():
    """
    Cria uma sessão de banco de dados isolada para cada teste unitário.
    Usa um arquivo SQLite temporário para garantir isolamento e persistência do schema.
    Aplica as migrations Alembic no banco temporário antes de iniciar a sessão.
    """
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_url = f"sqlite:///{tmpfile.name}"
    os.environ["DATABASE_URL"] = db_url
    logging.warning(f"[TEST] [UNIT] Criando banco temporário unitário: {tmpfile.name}")
    logging.warning(f"[TEST] [UNIT] Executando Alembic para {db_url}")
    result = subprocess.run(["alembic", "upgrade", "head"], check=True, env=os.environ.copy(), capture_output=True, text=True)
    logging.warning(f"[TEST] [UNIT] Alembic stdout: {result.stdout}")
    logging.warning(f"[TEST] [UNIT] Alembic stderr: {result.stderr}")
    logging.warning(f"[TEST] [UNIT] Banco existe após Alembic? {os.path.exists(tmpfile.name)}")
    engine = create_engine(db_url)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
        session.rollback()
    finally:
        session.close()
        engine.dispose()
        if os.path.exists(tmpfile.name):
            logging.warning(f"[TEST] [UNIT] Removendo banco temporário unitário: {tmpfile.name}")
            os.unlink(tmpfile.name)
        else:
            logging.warning(f"[TEST] [UNIT] Banco temporário unitário já removido: {tmpfile.name}")
