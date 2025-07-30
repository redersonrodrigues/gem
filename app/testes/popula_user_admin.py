import sqlite3
import hashlib

DB_PATH = "c:/Users/rrodrigues/Desktop/gem/app/database/escalas.db"


def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            perfil TEXT NOT NULL,
            ativo INTEGER NOT NULL DEFAULT 1
        );
    """)


def populate_user(conn):
    senha = "admin123"
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    try:
        conn.execute("""
            INSERT INTO user (nome, email, senha_hash, perfil, ativo)
            VALUES (?, ?, ?, ?, ?)
        """, ("Administrador", "admin@hospital.com", senha_hash, "admin_sistema", 1))
        conn.commit()
        print("Usuário de teste criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Usuário já existe.")


def main():
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)
    populate_user(conn)
    conn.close()


if __name__ == "__main__":
    main()
