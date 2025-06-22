import sys
import os
import hashlib
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.usuario import Usuario
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app', 'gem.db'))
print(f"Banco de dados em uso: {DB_PATH}")
engine = create_engine(f'sqlite:///{DB_PATH}')

with Session(engine) as session:
    usuarios = session.query(Usuario).all()
    print(f"Usuários cadastrados: {len(usuarios)}")
    for u in usuarios:
        print(f"login: {u.login}, hash: {u.senha_hash}, perfil: {u.perfil}, status: {u.status}")

print(f"Hash SHA-256 de '123456': {hashlib.sha256('123456'.encode('utf-8')).hexdigest()}")
print(f"Hash SHA-256 de 'admin': {hashlib.sha256('admin'.encode('utf-8')).hexdigest()}")
