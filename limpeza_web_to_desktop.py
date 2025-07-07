import os
import shutil

# Pastas e arquivos a remover (ajuste conforme necessário)
REMOVE_PATHS = [
    r'app/Templates',
    r'app/Control',
    r'Lib/Escala/Widgets',
    r'Lib/Escala/Control/Page.py',
    r'Lib/Escala/Control/action.py',
    r'Lib/Escala/Control/action_interface.py',
    r'app/Resources/form.html',
]

BACKUP_DIR = '_backup_web'

for path in REMOVE_PATHS:
    full_path = os.path.join(os.getcwd(), path)
    if os.path.exists(full_path):
        if os.path.isdir(full_path):
            print(f'Removendo diretório: {full_path}')
            shutil.rmtree(full_path)
        else:
            print(f'Removendo arquivo: {full_path}')
            os.remove(full_path)
    else:
        print(f'Não encontrado: {full_path}')

print('\nLimpeza definitiva concluída! Todos os arquivos/pastas foram removidos.')
