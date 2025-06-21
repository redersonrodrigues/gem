"""
Script para restauração do banco de dados SQLite (gem.db) a partir de um arquivo de backup.
Uso: python restore_db.py --backup-file <caminho_para_backup> [--db-path <destino>]
"""
import os
import shutil
import argparse

def restore_db(backup_file, db_path):
    if not os.path.exists(backup_file):
        print(f'Arquivo de backup não encontrado: {backup_file}')
        return
    shutil.copy2(backup_file, db_path)
    print(f'Banco de dados restaurado a partir de: {backup_file} para {db_path}')

def main():
    parser = argparse.ArgumentParser(description='Restaura banco SQLite a partir de backup.')
    parser.add_argument('--backup-file', type=str, required=True, help='Arquivo de backup de origem')
    parser.add_argument('--db-path', type=str, default=None, help='Caminho do banco SQLite de destino')
    args = parser.parse_args()
    db_path = args.db_path or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'gem.db'))
    restore_db(args.backup_file, db_path)

if __name__ == '__main__':
    main()
