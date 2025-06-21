"""
Script para exportar dados das tabelas principais do banco SQLite para arquivos CSV e JSON.
"""
import os
import sqlite3
import csv
import json
from datetime import datetime
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from app.core.database import init_db

EXPORT_DIR = os.path.join(os.path.dirname(__file__), 'exports')
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_table_to_csv(conn, table_name):
    try:
        cursor = conn.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        filename = os.path.join(EXPORT_DIR, f'{table_name}_{datetime.now():%Y%m%d_%H%M%S}.csv')
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f'[EXPORT] Exportado {len(rows)} registros da tabela {table_name} para {filename}')
        if len(rows) == 0:
            print(f'[EXPORT][WARN] Tabela {table_name} está vazia!')
        return filename
    except Exception as e:
        print(f'[EXPORT][ERRO] Falha ao exportar {table_name}: {e}')
        return None

def export_table_to_json(conn, table_name):
    try:
        cursor = conn.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        headers = [description[0] for description in cursor.description]
        data = [dict(zip(headers, row)) for row in rows]
        filename = os.path.join(EXPORT_DIR, f'{table_name}_{datetime.now():%Y%m%d_%H%M%S}.json')
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'[EXPORT] Exportado {len(data)} registros da tabela {table_name} para {filename}')
        if len(data) == 0:
            print(f'[EXPORT][WARN] Tabela {table_name} está vazia!')
        return filename
    except Exception as e:
        print(f'[EXPORT][ERRO] Falha ao exportar {table_name}: {e}')
        return None

def main():
    parser = argparse.ArgumentParser(description='Exporta tabelas do banco SQLite para CSV e JSON.')
    parser.add_argument('--db-path', type=str, default=None, help='Caminho do banco SQLite a ser exportado')
    args = parser.parse_args()

    db_path = args.db_path
    if db_path is None:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gem.db'))
    print(f"[DEBUG] Caminho do banco usado para exportação: {db_path}")

    # Garante que as tabelas existem no banco informado
    try:
        init_db(db_path)
    except Exception as e:
        print(f"[DEBUG] Não foi possível chamar init_db: {e}")

    tables = ['medicos', 'especializacoes', 'escalas_plantonistas', 'escalas_sobreaviso']
    conn = sqlite3.connect(db_path)
    for table in tables:
        try:
            print(f'[EXPORT] Exportando tabela {table}...')
            csv_file = export_table_to_csv(conn, table)
            json_file = export_table_to_json(conn, table)
        except Exception as e:
            print(f'[EXPORT][ERRO] Falha ao exportar {table}: {e}')
    conn.close()
    print('[EXPORT] Exportação concluída.')

if __name__ == '__main__':
    main()
