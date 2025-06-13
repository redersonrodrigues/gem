import pytest
from app.models.database import SessionLocal, init_db
from app.models.specialization import Specialization

def test_specializations_populated():
    init_db()
    session = SessionLocal()
    names = [
        "PLANTONISTA",
        "ORTOPEDISTA",
        "CLÍNICA MÉDICA",
        "CLÍNICA CIRÚRGICA",
        "G.O.",
        "PEDIATRA",
        "ANESTESISTA"
    ]
    for name in names:
        spec = session.query(Specialization).filter_by(name=name).first()
        assert spec is not None, f"Especialização {name} não encontrada no banco."
    session.close()
