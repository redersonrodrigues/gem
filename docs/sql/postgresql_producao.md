# Suporte a PostgreSQL: Replicação, Alta Disponibilidade e Escalabilidade

## Limitações do SQLite para Produção

- SQLite é recomendado apenas para ambientes de desenvolvimento, testes ou aplicações desktop de pequeno porte.
- Não suporta replicação nativa, alta disponibilidade, múltiplos acessos concorrentes em larga escala ou escalabilidade horizontal.
- Não possui recursos avançados de segurança, backup online, triggers complexos ou integração nativa com sistemas de replicação/cluster.

## Recomendações para Ambientes Maiores

- Para produção, utilize PostgreSQL, que oferece:
  - Replicação nativa (streaming replication, logical replication)
  - Alta disponibilidade (failover, hot standby, cluster)
  - Escalabilidade (conexões simultâneas, particionamento, sharding)
  - Segurança avançada (roles, criptografia, auditoria)
  - Ferramentas de backup/restore robustas
  - Suporte a extensões e integrações corporativas

## Exemplo de Configuração para PostgreSQL

### 1. Instale o PostgreSQL e o driver Python

No terminal do seu ambiente virtual:

```bash
pip install psycopg2-binary
```

Adicione ao `requirements.txt`:

```text
psycopg2-binary
```

### 2. String de Conexão

No arquivo de configuração ou `.env`:

```text
DATABASE_URL=postgresql+psycopg2://usuario:senha@localhost:5432/gem
```

### 3. Ajuste no `app/core/database.py`

Garanta que a função `get_engine` aceite a string de conexão PostgreSQL:

```python
from sqlalchemy import create_engine

def get_engine(db_url=None):
    if db_url is None:
        db_url = 'sqlite:///gem.db'  # padrão
    return create_engine(db_url, echo=False, future=True)
```

### 4. Uso no Projeto

Ao rodar a aplicação, passe a string de conexão PostgreSQL:

```python
from app.core.database import get_engine, get_session_local
engine = get_engine('postgresql+psycopg2://usuario:senha@localhost:5432/gem')
SessionLocal = get_session_local('postgresql+psycopg2://usuario:senha@localhost:5432/gem')
```

### 5. Migração de Dados

- Utilize Alembic para versionamento e migração do esquema.
- Exporte os dados do SQLite (CSV/JSON) e importe no PostgreSQL usando scripts já existentes.

### 6. Replicação e Alta Disponibilidade

- Configure a replicação nativa do PostgreSQL conforme a [documentação oficial](https://www.postgresql.org/docs/current/high-availability.html).
- Para alta disponibilidade, utilize ferramentas como Patroni, PgBouncer, repmgr ou soluções em nuvem (RDS, Cloud SQL, etc).

---

## Referências

- [Documentação Oficial PostgreSQL](https://www.postgresql.org/docs/)
- [SQLAlchemy Dialects - PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [Alembic - Migrations](https://alebric.sqlalchemy.org/en/latest/)
- [Patroni - HA PostgreSQL](https://github.com/zalando/patroni)
