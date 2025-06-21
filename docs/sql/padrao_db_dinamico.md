# Padrão de Uso Dinâmico do Caminho do Banco de Dados (SQLite)

## Objetivo

Permitir que toda a aplicação, scripts e testes utilizem dinamicamente o caminho do arquivo do banco de dados SQLite, facilitando:

- Execução de múltiplos ambientes (produção, desenvolvimento, testes, CI/CD)
- Isolamento de testes
- Backup, restauração, exportação e importação flexíveis
- Facilidade de integração e manutenção

## Como funciona

### 1. Core (`app/core/database.py`)

- Todas as funções principais (`init_db`, criação de engine/session) aceitam um argumento `db_path`.
- Se não informado, utiliza o caminho padrão (`gem.db` na raiz do projeto).
- Exemplo de uso:

```python
from app.core.database import init_db, get_engine, get_session_local

# Inicializa banco padrão
default_engine = get_engine()
init_db()

# Inicializa banco customizado
test_engine = get_engine(db_path='tests/tmp/teste.db')
init_db(db_path='tests/tmp/teste.db')
```

### 2. Scripts auxiliares

- Todos os scripts (`backup_db.py`, `restore_db.py`, `export_db.py`, `import_db.py`) aceitam o argumento `--db-path`.
- O caminho é repassado para o core e para o sqlite3, garantindo que todas as operações ocorram no arquivo correto.
- Exemplo de uso:

```sh
python scripts/backup_db.py --db-path tests/tmp/teste.db
python scripts/restore_db.py --backup-file scripts/backup/gem_backup_20250621_120000.db --db-path tests/tmp/teste.db
python scripts/export_db.py --db-path tests/tmp/teste.db
python scripts/import_db.py --db-path tests/tmp/teste.db
```

### 3. Testes automatizados

- Os testes de integração e unitários podem criar bancos temporários e passar o caminho para os scripts e para o core.
- Isso garante isolamento e evita conflitos entre execuções.

### 4. Variável de ambiente (opcional)

- O core suporta a variável de ambiente `GEM_DB_PATH` para definir o banco padrão globalmente.
- Útil para CI/CD ou ambientes específicos.

## Benefícios

- Flexibilidade para múltiplos ambientes
- Facilidade de manutenção e integração
- Testes mais robustos e isolados
- Scripts reutilizáveis e seguros

## Observações

- Sempre que possível, utilize o argumento `--db-path` nos scripts e informe o caminho explicitamente nos testes.
- O padrão é retrocompatível: se não informado, o banco padrão `gem.db` será utilizado.

---

**Última atualização:** 21/06/2025
