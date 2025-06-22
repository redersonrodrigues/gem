import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.usuario import Usuario, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'gem.db')
engine = create_engine(f'sqlite:///{DB_PATH}')

with Session(engine) as session:
    user = session.query(Usuario).filter_by(login='admin').first()
    if user:
        session.delete(user)
        session.commit()
        print('Usuário admin antigo removido.')
    novo_admin = Usuario(
        nome='Administrador',
        login='admin',
        perfil='admin',
        status=True
    )
    novo_admin.set_senha('123456')
    session.add(novo_admin)
    session.commit()
    print('Novo usuário admin criado com senha "123456".')
