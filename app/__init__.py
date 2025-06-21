# Inicialização do pacote app
from flask import Flask
from .database import init_db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gem.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    init_db(app)

    return app
# Aqui ficará o código principal da aplicação (MVC, controllers, serviços, etc)
