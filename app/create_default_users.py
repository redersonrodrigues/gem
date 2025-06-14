from app.models.database import SessionLocal, init_db
from app.models.user import User
from app.models.log import Log
from werkzeug.security import generate_password_hash

# Inicializa o banco e importa todos os modelos necessários
init_db()
session = SessionLocal()

# Cria usuário admin
if not session.query(User).filter_by(username='Admin').first():
    admin = User(username='Admin', password_hash=generate_password_hash('Admin'), is_admin=True)
    session.add(admin)
    print('Usuário Admin criado.')
else:
    print('Usuário Admin já existe.')

# Cria usuário comum
if not session.query(User).filter_by(username='User').first():
    user = User(username='User', password_hash=generate_password_hash('User'), is_admin=False)
    session.add(user)
    print('Usuário User criado.')
else:
    print('Usuário User já existe.')

session.commit()
session.close()
print('Processo concluído.')
