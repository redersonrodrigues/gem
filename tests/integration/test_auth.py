import pytest
from app.models.usuario import Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import usuario as usuario_model

# Setup banco de dados em memória para testes
@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    usuario_model.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def novo_usuario_admin(db_session):
    db_session.query(Usuario).delete()
    db_session.commit()
    user = Usuario(
        login="admin",
        nome="Administrador",
        perfil="admin"
    )
    user.set_senha("senha123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def novo_usuario_comum(db_session):
    db_session.query(Usuario).delete()
    db_session.commit()
    user = Usuario(
        login="usuario",
        nome="Usuário Comum",
        perfil="usuario"
    )
    user.set_senha("senha456")
    db_session.add(user)
    db_session.commit()
    return user

def test_login_valido_admin(db_session, novo_usuario_admin):
    user = db_session.query(Usuario).filter_by(login="admin").first()
    assert user is not None
    assert user.verificar_senha("senha123")
    assert user.is_admin()
    assert user.is_active()

def test_login_invalido(db_session, novo_usuario_admin):
    user = db_session.query(Usuario).filter_by(login="admin").first()
    assert not user.verificar_senha("senha_errada")

def test_login_valido_usuario_comum(db_session, novo_usuario_comum):
    user = db_session.query(Usuario).filter_by(login="usuario").first()
    assert user is not None
    assert user.verificar_senha("senha456")
    assert not user.is_admin()
    assert user.is_active()

def test_permissoes_admin(db_session, novo_usuario_admin):
    user = db_session.query(Usuario).filter_by(login="admin").first()
    assert user.perfil == "admin"
    assert user.is_admin()

def test_permissoes_usuario_comum(db_session, novo_usuario_comum):
    user = db_session.query(Usuario).filter_by(login="usuario").first()
    assert user.perfil == "usuario"
    assert not user.is_admin()
