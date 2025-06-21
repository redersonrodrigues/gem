import os
import shutil
import glob

# Caminho do banco de dados e pasta de backup
DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../gem.db')
)
BACKUP_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../backup')
)


def list_backups():
    files = sorted(
        glob.glob(os.path.join(BACKUP_DIR, 'gem_backup_*.db')),
        reverse=True
    )
    return files


def restore_database(backup_file):
    if not os.path.exists(backup_file):
        print(f'Backup não encontrado: {backup_file}')
        return
    shutil.copy2(backup_file, DB_PATH)
    print(f'Restaurado: {backup_file} -> {DB_PATH}')


if __name__ == '__main__':
    backups = list_backups()
    if not backups:
        print('Nenhum backup encontrado.')
    else:
        print('Backups disponíveis:')
        for i, bkp in enumerate(backups):
            print(f'{i+1}: {os.path.basename(bkp)}')
        idx = int(input('Escolha o número do backup para restaurar: ')) - 1
        if 0 <= idx < len(backups):
            restore_database(backups[idx])
        else:
            print('Opção inválida.')
