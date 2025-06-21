import sqlite3
import os

DB_PATH = r'F:\projetos\gem\gem.db'
VIEWS_SQL_PATH = os.path.join(os.path.dirname(__file__), 'views.sql')

def apply_views():
    with open(VIEWS_SQL_PATH, 'r', encoding='utf-8') as f:
        sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    try:
        with conn:
            conn.executescript(sql)
        print('Views aplicadas com sucesso!')
    except Exception as e:
        print(f'Erro ao aplicar views: {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    apply_views()
