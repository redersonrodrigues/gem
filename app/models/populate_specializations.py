# Script para popular especializações iniciais no banco de dados
from app.models.database import SessionLocal, init_db
from app.models.specialization import Specialization

SPECIALIZATIONS = [
    "PLANTONISTA",
    "ORTOPEDISTA",
    "CLÍNICA MÉDICA",
    "CLÍNICA CIRÚRGICA",
    "G.O.",
    "PEDIATRA",
    "ANESTESISTA",
]


def populate_specializations():
    session = SessionLocal()
    for name in SPECIALIZATIONS:
        exists = session.query(Specialization).filter_by(name=name).first()
        if not exists:
            session.add(Specialization(name=name))
    session.commit()
    session.close()


if __name__ == "__main__":
    init_db()
    populate_specializations()
    print("Especializações populadas com sucesso!")
