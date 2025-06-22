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
        user.senha_hash = hashlib.sha256('admin'.encode('utf-8')).hexdigest()
        session.commit()
        print('Senha do admin corrigida para "admin" (minúsculo).')
    else:
        print('Usuário admin não encontrado.')
