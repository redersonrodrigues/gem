from app.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Config

engine = create_engine(Config.DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    from app.models import doctor, hospital, specialization, schedule, user, log
    Base.metadata.create_all(bind=engine)
