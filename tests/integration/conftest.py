import subprocess
import os
import tempfile
import pytest
from app.core.database import get_session_local
from app.models.usuario import Usuario
from app.models.escala_plantonista import EscalaPlantonista
from app.models.medico import Medico
from app.models.especializacao import Especializacao
from datetime import date
from app.models import audit_listener  # Garante listeners ativos nos testes


@pytest.fixture(scope="session")
def banco_temp_integracao():
    """
    Cria um banco SQLite temporário para a sessão de testes de integração,
    aplica as migrations Alembic e retorna o caminho do banco.
    """
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_path = tmpfile.name
    db_url = f"sqlite:///{db_path}"
    os.environ["DATABASE_URL"] = db_url
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield db_path
    # Fecha conexões do SQLAlchemy e aguarda antes de remover o arquivo
    import time
    from sqlalchemy import create_engine
    import gc
    try:
        engine = create_engine(f"sqlite:///{db_path}")
        engine.dispose()
    except Exception:
        pass
    try:
        import sqlite3
        sqlite3.connect(db_path).close()
    except Exception:
        pass
    gc.collect()  # Força liberação de recursos pendentes
    time.sleep(2)  # Aguarda liberação do arquivo
    os.unlink(db_path)


@pytest.fixture(scope="session")
def session_factory(banco_temp_integracao):
    """
    Retorna uma factory de sessões SQLAlchemy para o banco temporário de integração.
    """
    db_url = f"sqlite:///{banco_temp_integracao}"

    def factory():
        SessionLocal = get_session_local(db_url)
        return SessionLocal()

    return factory


@pytest.fixture
def session(session_factory):
    db = session_factory()
    try:
        yield db
    finally:
        db.close()


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
