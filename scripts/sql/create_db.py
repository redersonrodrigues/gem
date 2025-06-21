"""
Script para criar o banco de dados SQLite (gem.db) e as tabelas iniciais:
- medicos
- especializacoes
- escalas_plantonistas
- escalas_sobreaviso

Este script pode ser executado manualmente ou via setup inicial.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '../..', 'gem.db')

def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de especializações
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS especializacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    );
    ''')

    # Tabela de médicos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nome_pj TEXT,
        especializacao_id INTEGER NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('ativo', 'inativo')),
        FOREIGN KEY (especializacao_id) REFERENCES especializacoes(id)
    );
    ''')

    # Tabela de escalas de plantonistas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS escalas_plantonistas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data DATE NOT NULL,
        turno TEXT NOT NULL CHECK(turno IN ('diurno', 'noturno')),
        medico1_id INTEGER NOT NULL,
        medico2_id INTEGER,
        FOREIGN KEY (medico1_id) REFERENCES medicos(id),
        FOREIGN KEY (medico2_id) REFERENCES medicos(id)
    );
    ''')

    # Tabela de escalas de sobreaviso
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS escalas_sobreaviso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_inicial DATE NOT NULL,
        data_final DATE NOT NULL,
        medico1_id INTEGER NOT NULL,
        especializacao_id INTEGER NOT NULL,
        FOREIGN KEY (medico1_id) REFERENCES medicos(id),
        FOREIGN KEY (especializacao_id) REFERENCES especializacoes(id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Banco de dados e tabelas criados com sucesso.")

if __name__ == "__main__":
    create_tables()
