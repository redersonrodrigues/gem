import sqlite3
from app.core.database import create_all_tables

conn = sqlite3.connect('gem.db')
cursor = conn.cursor()
try:
    cursor.execute("ALTER TABLE especializacoes ADD COLUMN version INTEGER DEFAULT 1;")
    print('Coluna version adicionada com sucesso!')
except Exception as e:
    print('Erro ao adicionar coluna version:', e)
conn.commit()
conn.close()

if __name__ == "__main__":
    create_all_tables()
    print('Tabelas criadas/atualizadas com sucesso!')
