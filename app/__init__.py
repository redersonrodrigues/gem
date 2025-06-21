# Inicialização do pacote app
try:
    from flask import Flask
except ImportError:
    Flask = None  # Permite rodar scripts/migrations sem Flask
from app.core.database import init_db, DEFAULT_DB_PATH


def create_app():
    if Flask is None:
        raise RuntimeError('Flask não está instalado. Instale Flask para rodar a aplicação web.')
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DEFAULT_DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    init_db()

    return app
# Aqui ficará o código principal da aplicação (MVC, controllers, serviços, etc)
