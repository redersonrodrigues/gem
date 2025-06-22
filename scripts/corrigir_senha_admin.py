import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.usuario import Usuario, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import hashlib

# Caminho absoluto do banco de dados usado pela aplicação
DB_PATH = r'F:\projetos\gem\gem.db'
print(f'Usando banco de dados: {DB_PATH}')
engine = create_engine(f'sqlite:///{DB_PATH}')

senha = 'admin'
hash_correto = hashlib.sha256(senha.encode('utf-8')).hexdigest()
print(f'Hash SHA-256 de "{senha}": {hash_correto}')

with Session(engine) as session:
    user = session.query(Usuario).filter_by(login='admin').first()
    if user:
        user.senha_hash = hash_correto
        session.commit()
        print('Senha do admin corrigida para "admin" (minúsculo).')
    else:
        print('Usuário admin não encontrado.')
