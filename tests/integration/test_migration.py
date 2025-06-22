import sqlite3
import pytest
import subprocess
import os
import uuid
from app.core.database import init_db
from sqlalchemy import create_engine, text

TMP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../tmp'))
os.makedirs(TMP_DIR, exist_ok=True)


@pytest.fixture
def src_db_path():
    db_path = os.path.join(TMP_DIR, f"src_{uuid.uuid4().hex}.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db(str(db_path))
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO especializacoes (nome, version) VALUES ('Clínica Geral', 1)"
    )
    especializacao_id = conn.execute(
        "SELECT id FROM especializacoes WHERE nome = 'Clínica Geral'"
    ).fetchone()[0]
    conn.execute(
        "INSERT INTO medicos (nome, nome_pj, especializacao_id, status, version) VALUES ('Dr. Teste', 'PJ Teste', ?, 'ativo', 1)",
        (especializacao_id,)
    )
    conn.commit()
    conn.close()
    # Garante que o arquivo existe e tem tamanho > 0
    assert os.path.exists(db_path), f"Arquivo {db_path} não existe!"
    assert os.path.getsize(db_path) > 0, f"Arquivo {db_path} está vazio!"
    return str(db_path)


@pytest.fixture
def dst_db_path():
    db_path = os.path.join(TMP_DIR, f"dst_{uuid.uuid4().hex}.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    # Não criar estrutura aqui! O script de migração deve assumir a estrutura.
    return str(db_path)


def test_migrate_medicos_especializacoes(src_db_path, dst_db_path):
    # Garante caminhos absolutos
    src_db_path = os.path.abspath(src_db_path)
    dst_db_path = os.path.abspath(dst_db_path)
    # Fecha conexões antes da migração
    # Executa migração apenas das tabelas medicos e especializacoes
    result = subprocess.run([
        'python', 'scripts/migrate_db.py',
        '--src-db', src_db_path,
        '--dst-db', dst_db_path,
        '--tables', 'medicos,especializacoes'
    ], capture_output=True, text=True)
    print("[MIGRATION STDOUT]\n" + result.stdout)
    assert result.returncode == 0, result.stderr
    # Verifica se os dados foram migrados usando SQLAlchemy
    engine = create_engine(f'sqlite:///{dst_db_path}')
    with engine.connect() as conn:
        medicos = conn.execute(text('SELECT nome, nome_pj, status, version FROM medicos')).fetchall()
        especializacoes = conn.execute(text('SELECT nome, version FROM especializacoes')).fetchall()
        print(f"[DEBUG] medicos: {medicos}")
        print(f"[DEBUG] especializacoes: {especializacoes}")
    assert ('Dr. Teste', 'PJ Teste', 'ativo', 1) in medicos
    assert ('Clínica Geral', 1) in especializacoes


def test_migrate_all_tables(src_db_path, dst_db_path):
    import os
    src_db_path = os.path.abspath(src_db_path)
    dst_db_path = os.path.abspath(dst_db_path)
    # Executa migração de todas as tabelas
    result = subprocess.run([
        'python', 'scripts/migrate_db.py',
        '--src-db', src_db_path,
        '--dst-db', dst_db_path
    ], capture_output=True, text=True)
    print("[MIGRATION STDOUT]\n" + result.stdout)
    assert result.returncode == 0, result.stderr
    # Verifica se os dados foram migrados usando SQLAlchemy
    engine = create_engine(f'sqlite:///{dst_db_path}')
    with engine.connect() as conn:
        medicos = conn.execute(text('SELECT nome, nome_pj, status, version FROM medicos')).fetchall()
        especializacoes = conn.execute(text('SELECT nome, version FROM especializacoes')).fetchall()
    assert ('Dr. Teste', 'PJ Teste', 'ativo', 1) in medicos
    assert ('Clínica Geral', 1) in especializacoes
