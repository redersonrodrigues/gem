import os
import sqlite3
import glob
import pytest
import time
from app.core.database import init_db, get_engine

EXPORT_SCRIPT = os.path.join(
    os.path.dirname(__file__), '../../scripts/export_db.py')
IMPORT_SCRIPT = os.path.join(
    os.path.dirname(__file__), '../../scripts/import_db.py')
BACKUP_SCRIPT = os.path.join(
    os.path.dirname(__file__), '../../scripts/backup_db.py')
RESTORE_SCRIPT = os.path.join(
    os.path.dirname(__file__), '../../scripts/restore_db.py')
DB_PATH = os.path.join(os.path.dirname(__file__), '../../gem.db')
EXPORT_DIR = os.path.join(os.path.dirname(__file__), '../../scripts/exports')
BACKUP_DIR = os.path.join(os.path.dirname(__file__), '../../scripts/backup')

@pytest.fixture
def db_path(banco_temp_integracao):
    return banco_temp_integracao

@pytest.fixture
def db_url(db_path):
    return f"sqlite:///{db_path}"

def run_script(script_path, args=None):
    cmd = f'python "{script_path}"'
    if args:
        cmd += f' {args}'
    assert os.system(cmd) == 0

def test_backup_and_restore(tmp_path, db_path):
    # Cria backup
    run_script(BACKUP_SCRIPT, f'--db-path "{db_path}"')
    backups = glob.glob(os.path.join(BACKUP_DIR, '*.db'))
    assert backups, 'Backup não foi criado.'
    backup_file = backups[-1]
    # Fecha conexões antes de manipular o arquivo
    import gc
    gc.collect()
    get_engine(db_path).dispose()  # Fecha conexões SQLAlchemy
    time.sleep(1)  # Aguarda liberação do arquivo
    # Remove DB original e restaura
    if os.path.exists(db_path + '.bak'):
        os.remove(db_path + '.bak')
    os.rename(db_path, db_path + '.bak')
    time.sleep(1)
    run_script(RESTORE_SCRIPT, f'--backup-file "{backup_file}" --db-path "{db_path}"')
    assert os.path.exists(db_path), 'Restauração falhou.'
    # Limpa
    os.remove(db_path)
    os.rename(db_path + '.bak', db_path)
    time.sleep(1)

def test_export_and_import(tmp_path, db_path):
    # Garante que as tabelas existem antes de exportar/importar
    init_db(db_path)
    # Insere dados de teste
    conn = sqlite3.connect(db_path)
    conn.execute("INSERT INTO especializacoes (id, nome, version) VALUES (1, 'Clínica', 1)")
    conn.execute("INSERT INTO medicos (id, nome, nome_pj, especializacao_id, status, version) VALUES (1, 'Dr. Teste', 'PJ Teste', 1, 'ativo', 1)")
    conn.execute("INSERT INTO escalas_plantonistas (id, data, turno, medico1_id, medico2_id, version) VALUES (1, '2025-06-21', 'diurno', 1, NULL, 1)")
    conn.execute("INSERT INTO escalas_sobreaviso (id, data_inicial, data_final, medico1_id, especializacao_id, version) VALUES (1, '2025-06-21', '2025-06-22', 1, 1, 1)")
    conn.commit()
    conn.close()
    # Exporta dados
    run_script(EXPORT_SCRIPT, f'--db-path "{db_path}"')
    csvs = glob.glob(os.path.join(EXPORT_DIR, '*.csv'))
    jsons = glob.glob(os.path.join(EXPORT_DIR, '*.json'))
    assert csvs, 'Exportação CSV não gerou arquivos.'
    assert jsons, 'Exportação JSON não gerou arquivos.'
    # Remove dados das tabelas
    conn = sqlite3.connect(db_path)
    tables = [
        'medicos',
        'especializacoes',
        'escalas_plantonistas',
        'escalas_sobreaviso',
    ]
    for table in tables:
        conn.execute(f'DELETE FROM {table}')
    conn.commit()
    conn.close()  # Fecha conexão antes de importar
    # Importa dados
    run_script(IMPORT_SCRIPT, f'--db-path "{db_path}"')
    # Verifica se dados foram restaurados
    conn = sqlite3.connect(db_path)
    for table in tables:
        cur = conn.execute(f'SELECT COUNT(*) FROM {table}')
        count = cur.fetchone()[0]
        assert count > 0, f'Tabela {table} não restaurada.'
    conn.close()
