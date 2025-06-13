import pytest
from app.models.database import init_db, SessionLocal
from app.models.user import User
from app.models.log import Log
import datetime

def test_create_log():
    init_db()
    session = SessionLocal()
    user = User(username="logtester", password_hash="hash", is_admin=False)
    session.add(user)
    session.commit()
    log = Log(user_id=user.id, action="CREATE", entity="Doctor", entity_id=1, timestamp=datetime.datetime.utcnow())
    session.add(log)
    session.commit()
    found = session.query(Log).filter_by(user_id=user.id, action="CREATE").first()
    assert found is not None
    assert found.entity == "Doctor"
    session.delete(found)
    session.delete(user)
    session.commit()
    session.close()
