import logging
import sqlite3
from typing import Optional

def check_integrity(db_path: str) -> bool:
    """Executa PRAGMA integrity_check e retorna True se o banco estiver íntegro."""
    conn = sqlite3.connect(db_path, timeout=1.0, check_same_thread=False)
    try:
        cur = conn.execute("PRAGMA integrity_check;")
        result = cur.fetchone()[0]
        logging.info(f"[MAINTENANCE] integrity_check: {result}")
        return result == 'ok'
    finally:
        conn.close()

def vacuum(db_path: str):
    """Executa VACUUM para otimizar o banco de dados."""
    conn = sqlite3.connect(db_path, timeout=1.0, check_same_thread=False)
    try:
        conn.execute("VACUUM;")
        logging.info("[MAINTENANCE] VACUUM executado com sucesso.")
    finally:
        conn.close()

def orphan_cleanup(db_path: str):
    """Remove médicos sem especialização válida (FK órfã ou nula)."""
    conn = sqlite3.connect(db_path, timeout=1.0, check_same_thread=False)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        # Buscar IDs órfãos
        cur = conn.execute(
            """
            SELECT m.id FROM medicos m
            LEFT JOIN especializacoes e ON m.especializacao_id = e.id
            WHERE e.id IS NULL
            """
        )
        ids = [row[0] for row in cur.fetchall()]
        if ids:
            conn.executemany("DELETE FROM medicos WHERE id = ?", [(i,) for i in ids])
            logging.info(f"[MAINTENANCE] Médicos órfãos removidos: {len(ids)}")
        else:
            logging.info("[MAINTENANCE] Nenhum médico órfão encontrado.")
    finally:
        conn.close()
