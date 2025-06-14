from app.models.base import Base
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.config import Config

# Otimização: Adicionado event listener para ativar PRAGMA de chaves estrangeiras no SQLite
engine = create_engine(Config.DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)

# Ativa PRAGMA de chaves estrangeiras para SQLite
if "sqlite" in Config.DATABASE_URI:

    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def init_db():
    from app.models import doctor, hospital, specialization, schedule, user, log

    Base.metadata.create_all(bind=engine)
