from flask import Flask
from app.database import init_db

# Inicialização do pacote app
# Aqui ficará o código principal da aplicação (MVC, controllers, serviços, etc)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../gem.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    init_db(app)
    return app