import sqlite3
import os

DB_PATH = r'F:\projetos\gem\gem.db'

# Função utilitária para exibir resultados de uma tabela
def print_table(cursor, table):
    print(f'\n--- {table.upper()} ---')
    for row in cursor.execute(f'SELECT * FROM {table} ORDER BY id'):
        print(row)

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print('==== ESTADO INICIAL DAS TABELAS ===')
    print_table(cursor, 'medicos')
    print_table(cursor, 'escalas_plantonistas')
    print_table(cursor, 'escalas_sobreaviso')

    # 1. Inserir um novo médico
    print('\n[TESTE] Inserindo novo médico...')
    cursor.execute("INSERT INTO medicos (nome, status, especializacao_id) VALUES (?, ?, ?)",
                   ('Dr. Trigger Teste', 'ativo', 1))
    conn.commit()
    print('[OK] Médico inserido.')
    print_table(cursor, 'medicos')

    # 2. Atualizar status do médico (deve acionar trigger se existir)
    print('\n[TESTE] Atualizando status do médico para inativo...')
    cursor.execute("UPDATE medicos SET status = 'inativo' WHERE nome = ?", ('Dr. Trigger Teste',))
    conn.commit()
    print('[OK] Status atualizado.')
    print_table(cursor, 'medicos')

    # 3. Inserir escala para o médico (plantonista)
    print('\n[TESTE] Inserindo escala PLANTONISTA para o médico...')
    medico_id = cursor.execute("SELECT id FROM medicos WHERE nome = ?", ('Dr. Trigger Teste',)).fetchone()[0]
    cursor.execute("INSERT INTO escalas_plantonistas (data, turno, medico1_id, medico2_id) VALUES (?, ?, ?, ?)",
                   ('2025-06-22', 'diurno', medico_id, None))
    conn.commit()
    print('[OK] Escala plantonista inserida.')
    print_table(cursor, 'escalas_plantonistas')

    # 4. Inserir escala para o médico (sobreaviso)
    print('\n[TESTE] Inserindo escala SOBREAVISO para o médico...')
    cursor.execute("INSERT INTO escalas_sobreaviso (data_inicial, data_final, medico1_id, especializacao_id) VALUES (?, ?, ?, ?)",
                   ('2025-06-23', '2025-06-24', medico_id, 1))
    conn.commit()
    print('[OK] Escala sobreaviso inserida.')
    print_table(cursor, 'escalas_sobreaviso')

    # 5. Remover médico (deve acionar trigger de integridade referencial)
    print('\n[TESTE] Tentando remover médico com escalas associadas...')
    try:
        cursor.execute("DELETE FROM medicos WHERE id = ?", (medico_id,))
        conn.commit()
        print('[ERRO] Médico removido, mas deveria ter sido bloqueado pelo trigger!')
    except sqlite3.IntegrityError as e:
        print(f'[OK] Trigger funcionou: {e}')
    print_table(cursor, 'medicos')
    print_table(cursor, 'escalas_plantonistas')
    print_table(cursor, 'escalas_sobreaviso')

    conn.close()
    print('\n==== FIM DOS TESTES DE TRIGGERS ===')

if __name__ == '__main__':
    main()
