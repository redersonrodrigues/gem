import pytest
from app.models.database import init_db, SessionLocal
from app.models.schedule import Schedule
from app.models.doctor import Doctor
from app.models.user import User
from app.models.log import Log
from datetime import datetime

def test_crud_schedule():
    init_db()
    session = SessionLocal()
    # Cria usuário admin
    user = User(username="admin_schedule", password_hash="hash", is_admin=True)
    session.add(user)
    session.commit()
    # Cria médicos
    doctor1 = Doctor(name="MEDICO1")
    doctor2 = Doctor(name="MEDICO2")
    session.add(doctor1)
    session.add(doctor2)
    session.commit()
    # CREATE
    escala = Schedule(data="2025-06-13", tipo="PLANTONISTA", medico1_id=doctor1.id, medico2_id=doctor2.id)
    session.add(escala)
    session.commit()
    log = Log(user_id=user.id, action='CREATE', entity='Schedule', entity_id=escala.id, timestamp=datetime.datetime.utcnow())
    session.add(log)
    session.commit()
    found = session.query(Schedule).filter_by(data="2025-06-13").first()
    assert found is not None
    # UPDATE
    found.medico2_id = doctor1.id
    session.commit()
    log = Log(user_id=user.id, action='UPDATE', entity='Schedule', entity_id=found.id, timestamp=datetime.datetime.utcnow())
    session.add(log)
    session.commit()
    found2 = session.query(Schedule).filter_by(data="2025-06-13").first()
    assert found2.medico2_id == doctor1.id
    # DELETE
    session.delete(found2)
    session.commit()
    log = Log(user_id=user.id, action='DELETE', entity='Schedule', entity_id=found2.id, timestamp=datetime.datetime.utcnow())
    session.add(log)
    session.commit()
    assert session.query(Schedule).filter_by(data="2025-06-13").first() is None
    # Limpeza
    session.delete(doctor1)
    session.delete(doctor2)
    session.delete(user)
    session.commit()
    session.close()
