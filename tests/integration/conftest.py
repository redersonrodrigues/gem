import sys
import os
# Adiciona o diretório absoluto de gem/ ao sys.path para garantir importação do pacote app
GEM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if GEM_PATH not in sys.path:
    sys.path.insert(0, GEM_PATH)

import subprocess
import tempfile
import pytest
from app.core.database import get_session_local
from app.models.usuario import Usuario
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from datetime import date
from app.models import audit_listener  # Garante listeners ativos nos testes
import uuid
import logging
import shutil
import time

logging.basicConfig(level=logging.WARNING, format='%(levelname)s:%(message)s')


@pytest.fixture(scope="function")
def banco_temp_integracao():
    """
    Cria um banco SQLite temporário para cada teste de integração,
    aplica as migrations Alembic e retorna o caminho do banco.
    """
    tmp_dir = os.path.join(os.path.dirname(__file__), "tmp")
    # Garante que o diretório tmp/ exista e esteja limpo
    try:
        os.makedirs(tmp_dir, exist_ok=True)
    except Exception as e:
        logging.error(f"[TEST] Erro ao criar pasta tmp/: {e}")
        raise
    if os.path.exists(tmp_dir):
        try:
            shutil.rmtree(tmp_dir)
        except Exception as e:
            logging.warning(f"[TEST] Falha ao limpar tmp/: {e}")
        try:
            os.makedirs(tmp_dir, exist_ok=True)
        except Exception as e:
            logging.error(f"[TEST] Erro ao recriar pasta tmp/: {e}")
            raise
    db_path = os.path.join(tmp_dir, f"test_{uuid.uuid4().hex}.db")
    db_url = f"sqlite:///{db_path}"
    os.environ["DATABASE_URL"] = db_url
    logging.warning(f"[TEST] [INTEGRACAO] Criando banco temporário: {db_path}")
    # Garante que o arquivo não existe antes
    if os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except Exception as e:
            logging.warning(f"[TEST] Falha ao remover banco antigo: {e}")
    # Cria o arquivo .db vazio antes de rodar o Alembic
    alembic_log_path = os.path.join(tmp_dir, f"alembic_log_{uuid.uuid4().hex}.txt")
    with open(db_path, 'wb') as f:
        pass
    print(f"[TEST][DEBUG] DATABASE_URL usada: {os.environ['DATABASE_URL']}")
    logging.warning(f"[TEST] [INTEGRACAO] DATABASE_URL usada: {os.environ['DATABASE_URL']}")
    logging.warning(f"[TEST] [INTEGRACAO] Executando Alembic para {db_url}")
    # Executa Alembic via API Python
    from alembic.config import Config
    from alembic import command
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), '../../migrations/alembic.ini'))
    alembic_cfg.set_main_option('script_location', os.path.join(os.path.dirname(__file__), '../../migrations'))
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)
    print(f"[TEST][DEBUG] DATABASE_URL usada: {db_url}")
    logging.warning(f"[TEST] [INTEGRACAO] DATABASE_URL usada: {db_url}")
    logging.warning(f"[TEST] [INTEGRACAO] Executando Alembic via API para {db_url}")
    try:
        command.upgrade(alembic_cfg, 'head')
    except Exception as e:
        logging.error(f"[TEST] Erro ao rodar Alembic via API: {e}")
        raise
    logging.warning(f"[TEST] [INTEGRACAO] Banco existe após Alembic? {os.path.exists(db_path)}")
    if not os.path.exists(db_path):
        logging.error(f"[TEST] Banco temporário não foi criado: {db_path}")
        raise AssertionError(f"Banco temporário não foi criado: {db_path}")
    return db_path


@pytest.fixture(scope="function")
def session_factory(banco_temp_integracao):
    """
    Retorna uma factory de sessões SQLAlchemy para o banco temporário de integração.
    """
    db_url = f"sqlite:///{banco_temp_integracao}"

    def factory():
        SessionLocal = get_session_local(db_url)
        return SessionLocal()

    return factory


@pytest.fixture(scope="function")
def session(session_factory, banco_temp_integracao):
    assert os.path.exists(banco_temp_integracao), f"Banco não existe: {banco_temp_integracao}"
    db = session_factory()
    try:
        yield db
    finally:
        db.close()
        import time
        from sqlalchemy import create_engine
        import gc
        try:
            engine = create_engine(f"sqlite:///{banco_temp_integracao}")
            engine.dispose()
        except Exception:
            pass
        try:
            import sqlite3
            sqlite3.connect(banco_temp_integracao).close()
        except Exception:
            pass
        gc.collect()
        time.sleep(1)
        if os.path.exists(banco_temp_integracao):
            logging.warning(f"[TEST] Removendo banco temporário: {banco_temp_integracao}")
            os.unlink(banco_temp_integracao)
        else:
            logging.warning(f"[TEST] Banco temporário já removido: {banco_temp_integracao}")


@pytest.fixture
def usuario_admin(session):
    """Cria e retorna um usuário admin válido para testes, removendo duplicatas."""
    session.query(Usuario).filter_by(login="admin").delete()
    session.commit()
    admin = Usuario(
        nome="Administrador de Teste",
        login="admin",
        perfil="admin",
        status=True
    )
    admin.set_senha("admin123")
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


@pytest.fixture
def escala_plantonista(session):
    """Cria e retorna uma escala de plantonista para testes de histórico/auditoria."""
    especializacao = session.query(Especializacao).first()
    if not especializacao:
        especializacao = Especializacao(nome="Clínica Geral")
        session.add(especializacao)
        session.commit()
    medico = session.query(Medico).first()
    if not medico:
        medico = Medico(nome="Dr. Teste", status="ativo", especializacao_id=especializacao.id)
        session.add(medico)
        session.commit()
    escala = EscalaPlantonista(medico1_id=medico.id, data=date(2024, 6, 10), turno="diurno")
    session.add(escala)
    session.commit()
    session.refresh(escala)
    return escala
