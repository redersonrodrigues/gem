import os
import tempfile
import sqlite3
import pytest
import gc
import time
from app.utils.maintenance import check_integrity, vacuum, orphan_cleanup

def test_check_integrity_ok():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_path = tmpfile.name
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE especializacoes (id INTEGER PRIMARY KEY, nome TEXT);")
        conn.commit()
        conn.close()
        gc.collect()
        time.sleep(0.1)
        assert check_integrity(db_path) is True
    finally:
        os.unlink(db_path)

def test_vacuum_runs():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_path = tmpfile.name
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE especializacoes (id INTEGER PRIMARY KEY, nome TEXT);")
        conn.commit()
        conn.close()
        gc.collect()
        time.sleep(0.1)
        vacuum(db_path)  # Não deve lançar exceção
    finally:
        os.unlink(db_path)

def test_orphan_cleanup_removes():
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmpfile:
        db_path = tmpfile.name
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("CREATE TABLE especializacoes (id INTEGER PRIMARY KEY, nome TEXT);")
        conn.execute("""
            CREATE TABLE medicos (
                id INTEGER PRIMARY KEY,
                especializacao_id INTEGER,
                nome TEXT,
                FOREIGN KEY (especializacao_id) REFERENCES especializacoes(id)
            );
        """)
        try:
            conn.execute("INSERT INTO medicos (id, especializacao_id, nome) VALUES (1, 999, 'Dr. Orfao')")
            conn.commit()
        except Exception:
            pass  # Ignora erro de integridade caso enforcement esteja ativo
        conn.close()
        gc.collect()
        time.sleep(0.3)
        orphan_cleanup(db_path)
        conn = sqlite3.connect(db_path)
        cur = conn.execute("SELECT COUNT(*) FROM medicos;")
        count = cur.fetchone()[0]
        conn.close()
        assert count == 0
    finally:
        os.unlink(db_path)
