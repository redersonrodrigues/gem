import os
import shutil
from datetime import datetime

# Caminho do banco de dados e pasta de backup
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../gem.db')
)
BACKUP_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../backup')
)


def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def backup_database():
    ensure_backup_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'gem_backup_{timestamp}.db')
    shutil.copy2(DB_PATH, backup_file)
    print(f'Backup realizado: {backup_file}')


if __name__ == '__main__':
    backup_database()
