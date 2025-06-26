from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
import os

# Caminho padrão para o banco de dados gem.db (sempre na raiz do projeto)
DEFAULT_DB_PATH = os.path.abspath(os.getenv('GEM_DB_PATH', r'gem.db'))

def get_engine(db_path=None, echo=True):
    path = db_path or DEFAULT_DB_PATH
    return create_engine(f'sqlite:///{path}', echo=echo)

def get_session_local(db_path=None, echo=True):
    engine = get_engine(db_path, echo)
    return sessionmaker(bind=engine)

def init_db(db_path=None, echo=True):
    engine = get_engine(db_path, echo)
    Base.metadata.create_all(bind=engine)

def create_all_tables():
    from app.models import usuario, especializacao, log
    Base.metadata.create_all(bind=get_engine())

# Exporta funções utilitárias e caminho padrão
__all__ = ['init_db', 'get_engine', 'get_session_local', 'DEFAULT_DB_PATH']
