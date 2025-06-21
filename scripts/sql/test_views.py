import sqlite3

# Validação das views SQL:
# Este script executa SELECT nas views criadas para garantir que estão acessíveis e retornando dados.
# Saída esperada: linhas das views ou mensagem de erro caso não existam.
#
# Para rodar: python scripts/sql/test_views.py
# Certifique-se de que o banco está populado e as views aplicadas.

conn = sqlite3.connect(r'F:\projetos\gem\gem.db')
cursor = conn.cursor()

print('vw_escalas_por_medico:')
cursor.execute('SELECT * FROM vw_escalas_por_medico LIMIT 5')
for row in cursor.fetchall():
    print(row)

print('\nvw_escalas_por_especializacao:')
cursor.execute('SELECT * FROM vw_escalas_por_especializacao LIMIT 5')
for row in cursor.fetchall():
    print(row)

print('\nvw_medicos_ativos_especializacoes:')
cursor.execute('SELECT * FROM vw_medicos_ativos_especializacoes LIMIT 5')
for row in cursor.fetchall():
    print(row)

conn.close()
