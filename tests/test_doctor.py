import pytest
from app.models.database import init_db, SessionLocal
from app.models.doctor import Doctor
from app.models.specialization import Specialization
from app.models.user import User
from app.models.log import Log
from datetime import datetime
import datetime
from datetime import timezone


def test_crud_doctor():
    init_db()
    session = SessionLocal()
    # Remove especialização, usuário e médico se já existirem
    session.query(Doctor).filter_by(name="MEDICO TESTE").delete()
    session.query(Doctor).filter_by(name="MEDICO TESTE EDITADO").delete()
    session.query(Specialization).filter_by(name="TESTE").delete()
    session.query(User).filter_by(username="admin_doctor").delete()
    session.commit()
    # Cria especialização
    spec = Specialization(name="TESTE")
    session.add(spec)
    session.commit()
    # Cria usuário admin
    user = User(username="admin_doctor", password_hash="hash", is_admin=True)
    session.add(user)
    session.commit()
    # CREATE
    doctor = Doctor(name="MEDICO TESTE", fantasy_name="FANTASIA TESTE")
    doctor.specializations.append(spec)
    session.add(doctor)
    session.commit()
    log = Log(
        user_id=user.id,
        action="CREATE",
        entity="Doctor",
        entity_id=doctor.id,
        timestamp=datetime.datetime.now(timezone.utc),
    )
    session.add(log)
    session.commit()
    found = session.query(Doctor).filter_by(name="MEDICO TESTE").first()
    assert found is not None
    # UPDATE
    found.name = "MEDICO TESTE EDITADO"
    session.commit()
    log = Log(
        user_id=user.id,
        action="UPDATE",
        entity="Doctor",
        entity_id=found.id,
        timestamp=datetime.datetime.now(timezone.utc),
    )
    session.add(log)
    session.commit()
    found2 = session.query(Doctor).filter_by(
        name="MEDICO TESTE EDITADO").first()
    assert found2 is not None
    # DELETE
    session.delete(found2)
    session.commit()
    log = Log(
        user_id=user.id,
        action="DELETE",
        entity="Doctor",
        entity_id=found2.id,
        timestamp=datetime.datetime.now(timezone.utc),
    )
    session.add(log)
    session.commit()
    assert session.query(Doctor).filter_by(
        name="MEDICO TESTE EDITADO").first() is None
    # Limpeza
    session.delete(user)
    session.delete(spec)
    session.commit()
    session.close()
