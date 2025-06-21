import sqlite3
import os

# Caminhos dos arquivos
DB_PATH = r'F:\projetos\gem\gem.db'
TRIGGERS_PATH = os.path.join(os.path.dirname(__file__), 'triggers.sql')

def aplicar_triggers():
    with open(TRIGGERS_PATH, 'r', encoding='utf-8') as f:
        sql = f.read()
    # Conecta ao banco e executa o script
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        try:
            cursor.executescript(sql)
            print('Triggers aplicados com sucesso!')
        except Exception as e:
            print(f'Erro ao aplicar triggers: {e}')
        finally:
            cursor.close()

if __name__ == '__main__':
    aplicar_triggers()
