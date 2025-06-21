from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
import os

# Caminho absoluto para o banco de dados gem.db
DB_PATH = r'F:\projetos\gem\gem.db'
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

# Exporta DB_PATH para importação externa
__all__ = ['init_db', 'DB_PATH']
