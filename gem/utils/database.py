# Configuração do banco de dados
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Inicializa o banco de dados com a aplicação Flask"""
    db.init_app(app)
    with app.app_context():
        db.create_all()


def get_db_config():
    """Retorna a configuração padrão do banco de dados"""
    return {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///gem.db',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }