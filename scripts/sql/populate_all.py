"""
Script Python para popular o banco de dados gem.db com os dados de exemplo das tabelas:
- especializacoes
- medicos
- escalas_plantonistas
- escalas_sobreaviso
"""
import sqlite3
import os

DB_PATH = r'F:\projetos\gem\gem.db'
SCRIPTS = [
    'populate_especializacoes.sql',
    'populate_medicos.sql',
    'populate_escalas.sql',
]

SQL_DIR = os.path.dirname(os.path.abspath(__file__))

def run_scripts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        for script in SCRIPTS:
            script_path = os.path.join(SQL_DIR, script)
            with open(script_path, 'r', encoding='utf-8') as f:
                sql = f.read()
                cursor.executescript(sql)
                print(f"Script {script} executado com sucesso.")
        conn.commit()
        print("Todos os scripts executados com sucesso!")
    except Exception as e:
        print(f"Erro ao executar scripts: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_scripts()
