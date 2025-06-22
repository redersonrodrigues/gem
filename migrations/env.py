import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sqlite3

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models import Base  # importa o Base dos modelos (inclui todos)

config = context.config
fileConfig(config.config_file_name)
target_metadata = Base.metadata

# Lê a variável de ambiente DATABASE_URL, se existir, e sobrescreve a configuração
if "DATABASE_URL" in os.environ:
    db_url = os.environ["DATABASE_URL"]
    config.set_main_option("sqlalchemy.url", db_url)


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
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
        run_post_migration_sql_scripts()


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
    run_migrations_online()
