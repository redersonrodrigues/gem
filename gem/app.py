# Configuração principal da aplicação Flask
from flask import Flask
from gem.utils.database import init_db, get_db_config, db
from flask_migrate import Migrate


def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração do banco de dados
    db_config = get_db_config()
    app.config.update(db_config)
    
    # Inicializar o banco de dados
    init_db(app)
    
    # Configurar Flask-Migrate
    migrate = Migrate(app, db)
    
    # Registrar blueprints/rotas aqui quando necessário
    # from gem.views import register_routes
    # register_routes(app)
    
    return app


# Função para popular dados iniciais
def populate_initial_data():
    """Popula dados iniciais no banco de dados"""
    from gem.services.especializacao_service import EspecializacaoService
    
    especializacao_service = EspecializacaoService()
    especializacao_service.popular_especializacoes_iniciais()
    print("Dados iniciais populados com sucesso!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        populate_initial_data()
    app.run(debug=True)