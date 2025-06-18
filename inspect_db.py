from app import create_app
from app.database import db
from sqlalchemy import text


def inspect_db():
    with app.app_context():
        tables = db.session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
        print("\nEstrutura completa do banco de dados:\n")
        for table in tables:
            print(f"Tabela: {table[0]}")
            columns = db.session.execute(
                text(f"PRAGMA table_info({table[0]});")).fetchall()
            for column in columns:
                print(f"  Coluna: {column[1]} - Tipo: {column[2]}")
            print("-")

        print("\nRelacionamentos:\n")
        for table in tables:
            foreign_keys = db.session.execute(
                text(f"PRAGMA foreign_key_list({table[0]});")).fetchall()
            if foreign_keys:
                print(
                    f"Tabela: {table[0]} possui as seguintes chaves estrangeiras:")
                for fk in foreign_keys:
                    print(
                        f"  Coluna: {fk[3]} -> Tabela Referenciada: {fk[2]} (Coluna: {fk[4]})")
            else:
                print(f"Tabela: {table[0]} não possui chaves estrangeiras.")
            print("-")


if __name__ == "__main__":
    app = create_app()
    inspect_db()
