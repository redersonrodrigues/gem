"""
Script para validar a estrutura das tabelas do banco gem.db usando SQLAlchemy.
"""
from sqlalchemy import create_engine, inspect

engine = create_engine('sqlite:///gem.db')
inspector = inspect(engine)

tables = inspector.get_table_names()
print("Tabelas encontradas:")
for table in tables:
    print(f"- {table}")
    columns = inspector.get_columns(table)
    print("  Colunas:")
    for col in columns:
        print(f"    - {col['name']} ({col['type']})")
    print()
