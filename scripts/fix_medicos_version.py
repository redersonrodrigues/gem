import sqlite3

DB_PATH = 'gem.db'

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Verifica se a coluna 'version' já existe
cur.execute("PRAGMA table_info(medicos);")
columns = [col[1] for col in cur.fetchall()]

if 'version' not in columns:
    print('Corrigindo tabela medicos: adicionando coluna version...')
    # Cria tabela temporária com a coluna version
    cur.execute('''
        CREATE TABLE IF NOT EXISTS medicos_temp (
            id INTEGER PRIMARY KEY,
            nome TEXT,
            nome_pj TEXT,
            especializacao_id INTEGER,
            status INTEGER,
            version INTEGER DEFAULT 1
        )
    ''')
    # Copia os dados da tabela antiga para a nova, preenchendo version=1
    cur.execute('''
        INSERT INTO medicos_temp (id, nome, nome_pj, especializacao_id, status, version)
        SELECT id, nome, nome_pj, especializacao_id, status, 1 FROM medicos
    ''')
    # Renomeia as tabelas
    cur.execute('ALTER TABLE medicos RENAME TO medicos_old')
    cur.execute('ALTER TABLE medicos_temp RENAME TO medicos')
    conn.commit()
    print('Tabela medicos corrigida com a coluna version!')
else:
    print('A coluna version já existe na tabela medicos.')

conn.close()