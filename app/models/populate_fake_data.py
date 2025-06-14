import random
import datetime
from abc import ABC, abstractmethod
from sqlalchemy import text
from app.models.database import SessionLocal, init_db
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.schedule import Schedule
from sqlalchemy import Column, Date


# Classe abstrata para Escala (Template Method)
class Escala(ABC):
    def __init__(self, session, data):
        self.session = session
        self.data = data

    @abstractmethod
    def criar(self, *args, **kwargs):
        pass


class Plantonista(Escala):
    def criar(self, doctors):
        plantonistas = random.sample(doctors, 4)
        schedule = Schedule(
            data=self.data,
            diurno_medico1_id=plantonistas[0].id,
            diurno_medico2_id=plantonistas[1].id,
            noturno_medico1_id=plantonistas[2].id,
            noturno_medico2_id=plantonistas[3].id,
            tipo="PLANTONISTA",
        )
        self.session.add(schedule)


class SobreavisoOrtopedia(Escala):
    def criar(self, doctors):
        ortopedia = random.choice(doctors)
        schedule = Schedule(
            data=self.data, ortopedia_medico_id=ortopedia.id, tipo="SOBREAVISO_ORTOPEDIA"
        )
        self.session.add(schedule)


class SobreavisoOutras(Escala):
    def criar(self, doctors, especialidade):
        sobreaviso = random.choice(doctors)
        schedule = Schedule(
            data=self.data,
            sobreaviso_especialidade=especialidade,
            sobreaviso_medico_id=sobreaviso.id,
            tipo="SOBREAVISO_OUTRAS",
        )
        self.session.add(schedule)


def random_name(prefix, idx):
    return f"{prefix.upper()}_{idx:03d}"


def populate_doctors(session, n=100):
    specializations = session.query(Specialization).all()
    doctors = []
    for i in range(1, n + 1):
        name = random_name("MEDICO", i)
        fantasy_name = random_name("FANTASIA", i)
        specs = random.sample(
            specializations, k=random.randint(1, min(3, len(specializations)))
        )
        doctor = Doctor(
            name=name, fantasy_name=fantasy_name, specializations=list(set(specs))
        )
        session.add(doctor)
        doctors.append(doctor)
    session.commit()
    return doctors


def populate_plantonistas(session, doctors, n=30):
    start_date = datetime.date.today()
    for i in range(n):
        data = start_date + datetime.timedelta(days=i)
        escala = Plantonista(session, data)
        escala.criar(doctors)
    session.commit()


def populate_sobreaviso_ortopedia(session, doctors, n=2):
    start_date = datetime.date.today()
    for i in range(n):
        data = start_date + datetime.timedelta(days=i * 15)
        escala = SobreavisoOrtopedia(session, data)
        escala.criar(doctors)
    session.commit()


def populate_sobreaviso_outras(session, doctors, specializations, n_weeks=4):
    start_date = datetime.date.today()
    for spec in specializations:
        if spec.name == "ORTOPEDISTA":
            continue
        for i in range(n_weeks):
            data = start_date + datetime.timedelta(days=i * 7)
            escala = SobreavisoOutras(session, data)
            escala.criar(doctors, especialidade=spec.name)
    session.commit()


def main():
    init_db()
    session = SessionLocal()
    session.execute(text("DELETE FROM doctor_specialization"))
    session.query(Schedule).delete()
    session.query(Doctor).delete()
    session.commit()
    if session.query(Specialization).count() == 0:
        print("Popule as especializações antes de rodar este script.")
        return
    doctors = populate_doctors(session, 100)
    specializations = session.query(Specialization).all()
    populate_plantonistas(session, doctors, n=30)
    populate_sobreaviso_ortopedia(session, doctors, n=2)
    populate_sobreaviso_outras(session, doctors, specializations, n_weeks=4)
    print(
        "Médicos e escalas (plantonistas, sobreaviso ortopedia, sobreaviso outras) populados com sucesso!"
    )
    session.close()


if __name__ == "__main__":
    main()
