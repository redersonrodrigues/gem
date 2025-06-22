import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sqlite3
import logging

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Base  # importa o Base dos modelos (inclui todos)

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Lê a variável de ambiente DATABASE_URL, se existir, e sobrescreve a configuração
if "DATABASE_URL" in os.environ:
    db_url = os.environ["DATABASE_URL"]
    print(f"[ALEMBIC][DEBUG] DATABASE_URL detectada: {db_url}", flush=True)
    logging.warning(f"[Alembic][DEBUG] DATABASE_URL detectada: {db_url}")
    config.set_main_option("sqlalchemy.url", db_url)
else:
    print(f"[ALEMBIC][DEBUG] DATABASE_URL não detectada. Usando sqlalchemy.url padrão: {config.get_main_option('sqlalchemy.url')}", flush=True)
    logging.warning(f"[Alembic][DEBUG] DATABASE_URL não detectada. Usando sqlalchemy.url padrão: {config.get_main_option('sqlalchemy.url')}")

print(f"[ALEMBIC][DEBUG] Iniciando processo de migration. Modo offline: {context.is_offline_mode()}", flush=True)

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    db_url = config.get_main_option("sqlalchemy.url")
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        print(f"[ALEMBIC][DEBUG] Caminho do banco SQLite: {db_path}", flush=True)
    try:
        with connectable.connect() as connection:
            context.configure(
                connection=connection, target_metadata=target_metadata
            )
            print("[ALEMBIC][DEBUG] Conexão estabelecida. Iniciando migrations...", flush=True)
            with context.begin_transaction():
                context.run_migrations()
            print("[ALEMBIC][DEBUG] Migrations concluídas. Executando scripts pós-migration...", flush=True)
            run_post_migration_sql_scripts()
            print("[ALEMBIC][DEBUG] Scripts pós-migration concluídos.", flush=True)
    except Exception as e:
        import traceback
        print(f"[ALEMBIC][ERRO] Exceção durante run_migrations_online: {e}", flush=True)
        traceback.print_exc()
        raise


def run_post_migration_sql_scripts():
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'sql')
    db_url = config.get_main_option("sqlalchemy.url")
    if db_url.startswith("sqlite:///"):
        db_path = db_url.replace("sqlite:///", "")
        if os.path.exists(db_path):
            conn = sqlite3.connect(db_path)
            for script in ["views.sql", "triggers.sql", "indexes.sql", "populate_especializacoes.sql", "populate_medicos.sql", "populate_escalas.sql"]:
                script_path = os.path.join(sql_dir, script)
                if os.path.exists(script_path):
                    with open(script_path, "r", encoding="utf-8") as f:
                        sql = f.read()
                        try:
                            conn.executescript(sql)
                        except Exception as e:
                            print(f"[Alembic][WARN] Erro ao aplicar {script}: {e}")
            conn.close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    try:
        run_migrations_online()
        print("[ALEMBIC][DEBUG] Processo de migration finalizado com sucesso.", flush=True)
    except Exception as e:
        import traceback
        print(f"[ALEMBIC][ERRO] {e}", flush=True)
        traceback.print_exc()
        raise
