import random
import datetime
from sqlalchemy import text
from app.models.database import SessionLocal, init_db
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.plantonista import Plantonista
from app.models.sobreaviso import Sobreaviso


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
        plantonistas = random.sample(doctors, 4)
        escala = Plantonista(
            data=data,
            diurno_medico1_id=plantonistas[0].id,
            diurno_medico2_id=plantonistas[1].id,
            noturno_medico1_id=plantonistas[2].id,
            noturno_medico2_id=plantonistas[3].id,
        )
        session.add(escala)
    session.commit()


def populate_sobreavisos(session, doctors, specializations, n_weeks=4):
    start_date = datetime.date.today()
    for spec in specializations:
        for i in range(n_weeks):
            data = start_date + datetime.timedelta(days=i * 7)
            medico = random.choice(doctors)
            sobreaviso = Sobreaviso(
                data=data,
                especialidade=spec.name,
                medico_id=medico.id,
            )
            session.add(sobreaviso)
    session.commit()


def main():
    init_db()
    session = SessionLocal()
    session.execute(text("DELETE FROM doctor_specialization"))
    session.query(Plantonista).delete()
    session.query(Sobreaviso).delete()
    session.query(Doctor).delete()
    session.commit()
    if session.query(Specialization).count() == 0:
        print("Popule as especializações antes de rodar este script.")
        return
    doctors = populate_doctors(session, 100)
    specializations = session.query(Specialization).all()
    populate_plantonistas(session, doctors, n=30)
    populate_sobreavisos(session, doctors, specializations, n_weeks=4)
    print("Médicos, plantonistas e sobreavisos populados com sucesso!")
    session.close()


if __name__ == "__main__":
    main()
