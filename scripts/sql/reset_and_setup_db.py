import os
import subprocess
import sys

DB_PATH = r'F:\projetos\gem\gem.db'

scripts = [
    'create_db.py',
    'populate_all.py',
    'apply_triggers.py',
    'apply_views.py',
]

if os.path.exists(DB_PATH):
    print(f'Removendo banco antigo: {DB_PATH}')
    os.remove(DB_PATH)
else:
    print('Nenhum banco antigo encontrado, prosseguindo...')

for script in scripts:
    script_path = os.path.join(os.path.dirname(__file__), script)
    print(f'Executando: {script}')
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f'Erro ao executar {script}:')
        print(result.stderr)
        break
print('Setup do banco concluído!')
