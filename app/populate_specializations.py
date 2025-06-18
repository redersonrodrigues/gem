from app.models import Especializacao
from app.database import db
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Script para popular especializações iniciais


def popular_especializacoes():
    especializacoes_iniciais = [
        "Cardiologia",
        "Ortopedia",
        "Pediatria",
        "Neurologia",
        "Dermatologia"
    ]

    for nome in especializacoes_iniciais:
        if not Especializacao.query.filter_by(nome=nome.upper()).first():
            especializacao = Especializacao(nome=nome)
            db.session.add(especializacao)

    db.session.commit()


if __name__ == "__main__":
    from app import create_app

    app = create_app()
    with app.app_context():
        popular_especializacoes()
        print("Especializações iniciais populadas com sucesso!")
