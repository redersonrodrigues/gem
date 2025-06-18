# Inicialização do pacote app
from flask import Flask
from .database import init_db
from flask_migrate import Migrate
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gem.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar o banco de dados
    init_db(app)

    # Configurar Flask-Migrate
    migrate = Migrate(app, db)

    return app
