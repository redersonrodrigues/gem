from app.models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    from app.models import doctor, hospital, specialization, schedule, user, log
    Base.metadata.create_all(bind=engine)
