import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.usuario import Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'gem.db'))
engine = create_engine(f'sqlite:///{DB_PATH}')

with Session(engine) as session:
    user = session.query(Usuario).filter_by(login='admin').first()
    if user:
        print('Usuário admin encontrado.')
        print('Senha "123456" confere?', user.verificar_senha('123456'))
        print('Senha "admin" confere?', user.verificar_senha('admin'))
    else:
        print('Usuário admin não encontrado.')
