import pytest
from app.models.database import init_db, SessionLocal
from app.models.specialization import Specialization
from app.models.user import User
from app.models.log import Log
from datetime import datetime


def test_crud_specialization():
    init_db()
    session = SessionLocal()
    # Remove usuário e especialização se já existirem
    session.query(Specialization).filter_by(name="ESPECIAL TESTE").delete()
    session.query(Specialization).filter_by(name="ESPECIAL TESTE EDITADO").delete()
    session.query(User).filter_by(username="admin_spec").delete()
    session.commit()
    # Cria usuário admin
    user = User(username="admin_spec", password_hash="hash", is_admin=True)
    session.add(user)
    session.commit()
    # CREATE
    spec = Specialization(name="ESPECIAL TESTE")
    session.add(spec)
    session.commit()
    log = Log(
        user_id=user.id,
        action="CREATE",
        entity="Specialization",
        entity_id=spec.id,
        timestamp=datetime.utcnow(),
    )
    session.add(log)
    session.commit()
    found = session.query(Specialization).filter_by(name="ESPECIAL TESTE").first()
    assert found is not None
    # UPDATE
    found.name = "ESPECIAL TESTE EDITADO"
    session.commit()
    log = Log(
        user_id=user.id,
        action="UPDATE",
        entity="Specialization",
        entity_id=found.id,
        timestamp=datetime.utcnow(),
    )
    session.add(log)
    session.commit()
    found2 = (
        session.query(Specialization).filter_by(name="ESPECIAL TESTE EDITADO").first()
    )
    assert found2 is not None
    # DELETE
    session.delete(found2)
    session.commit()
    log = Log(
        user_id=user.id,
        action="DELETE",
        entity="Specialization",
        entity_id=found2.id,
        timestamp=datetime.utcnow(),
    )
    session.add(log)
    session.commit()
    assert (
        session.query(Specialization).filter_by(name="ESPECIAL TESTE EDITADO").first()
        is None
    )
    # Limpeza
    session.delete(user)
    session.commit()
    session.close()
