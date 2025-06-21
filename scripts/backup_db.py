"""
Script para backup do banco de dados SQLite (gem.db).
Cria uma cópia do banco com timestamp na pasta backup/.
"""
import os
import shutil
from datetime import datetime
import argparse

BACKUP_DIR = os.path.join(os.path.dirname(__file__), 'backup')

def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def backup_db(db_path):
    ensure_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = os.path.splitext(os.path.basename(db_path))[0]
    backup_file = os.path.join(BACKUP_DIR, f'{base_name}_backup_{timestamp}.db')
    shutil.copy2(db_path, backup_file)
    print(f'Backup criado: {backup_file}')

def main():
    parser = argparse.ArgumentParser(description='Backup do banco de dados SQLite.')
    parser.add_argument('--db-path', type=str, default=None, help='Caminho do banco SQLite a ser copiado')
    args = parser.parse_args()
    db_path = args.db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gem.db'))
    backup_db(db_path)

if __name__ == '__main__':
    main()
