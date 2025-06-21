# Inicialização do pacote app
from flask import Flask
from app.core.database import init_db, DB_PATH


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    init_db()

    return app
# Aqui ficará o código principal da aplicação (MVC, controllers, serviços, etc)
