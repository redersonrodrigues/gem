from app import create_app
from app.database import db
from sqlalchemy import text


def apply_sql_script(file_path):
    with open(file_path, 'r') as file:
        sql_script = file.read()

    with app.app_context():
        with db.engine.connect() as connection:
            for statement in sql_script.split(';'):
                if statement.strip():
                    try:
                        connection.execute(text(statement))
                    except Exception as e:
                        print(f"Erro ao executar: {statement.strip()}\n{e}")


if __name__ == "__main__":
    app = create_app()
    apply_sql_script('recreate_tables.sql')
