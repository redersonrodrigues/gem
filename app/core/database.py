from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'gem.db')
engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
