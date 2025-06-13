import pytest
from app.models.database import init_db, SessionLocal
from app.models.user import User

def test_create_user():
    init_db()
    session = SessionLocal()
    user = User(username="admin", password_hash="hash", is_admin=True)
    session.add(user)
    session.commit()
    found = session.query(User).filter_by(username="admin").first()
    assert found is not None
    assert found.is_admin is True
    session.delete(found)
    session.commit()
    session.close()
