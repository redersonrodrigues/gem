import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.models.usuario import Usuario, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'gem.db')
engine = create_engine(f'sqlite:///{DB_PATH}')

# Criação do usuário admin
usuario_admin = Usuario(
    nome='Administrador',
    login='admin',
    perfil='admin',
    status=True
)
usuario_admin.set_senha('admin')

Base.metadata.create_all(engine)

with Session(engine) as session:
    existe = session.query(Usuario).filter_by(login='admin').first()
    if existe:
        print('Usuário admin já existe.')
    else:
        session.add(usuario_admin)
        session.commit()
        print('Usuário admin criado com sucesso!')
