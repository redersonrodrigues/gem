"""
Script para importar dados de arquivos CSV ou JSON para as tabelas principais do banco SQLite.
"""
import os
import sqlite3
import csv
import json
import glob
import argparse

def import_csv_to_table(conn, table_name, file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        print(f'[IMPORT] Lendo {file_path}: {len(rows)} registros encontrados.')
        if not rows:
            print(f'[IMPORT][WARN] Arquivo CSV vazio: {file_path}')
            return
        columns = rows[0].keys()
        placeholders = ','.join(['?'] * len(columns))
        sql = f'INSERT OR REPLACE INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
        values = [tuple(row[col] for col in columns) for row in rows]
        conn.executemany(sql, values)
        print(f'[IMPORT] Importados {len(rows)} registros para {table_name} de {file_path}')

def import_json_to_table(conn, table_name, file_path):
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
        print(f'[IMPORT] Lendo {file_path}: {len(data)} registros encontrados.')
        if not data:
            print(f'[IMPORT][WARN] Arquivo JSON vazio: {file_path}')
            return
        columns = data[0].keys()
        placeholders = ','.join(['?'] * len(columns))
        sql = f'INSERT OR REPLACE INTO {table_name} ({",".join(columns)}) VALUES ({placeholders})'
        values = [tuple(row[col] for col in columns) for row in data]
        conn.executemany(sql, values)
        print(f'[IMPORT] Importados {len(data)} registros para {table_name} de {file_path}')

def main():
    parser = argparse.ArgumentParser(description='Importa dados CSV/JSON para o banco SQLite.')
    parser.add_argument('--db-path', type=str, default=None, help='Caminho do banco SQLite a ser importado')
    args = parser.parse_args()
    db_path = args.db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gem.db'))
    tables = ['medicos', 'especializacoes', 'escalas_plantonistas', 'escalas_sobreaviso']
    import_dir = os.path.join(os.path.dirname(__file__), 'exports')
    conn = sqlite3.connect(db_path)
    for table in tables:
        print(f'[IMPORT] Importando dados para tabela {table}...')
        csv_files = glob.glob(os.path.join(import_dir, f'{table}_*.csv'))
        json_files = glob.glob(os.path.join(import_dir, f'{table}_*.json'))
        for file_path in csv_files:
            import_csv_to_table(conn, table, file_path)
        for file_path in json_files:
            import_json_to_table(conn, table, file_path)
    conn.commit()
    conn.close()
    print('[IMPORT] Importação concluída.')

if __name__ == '__main__':
    main()
