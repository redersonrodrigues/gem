# Padrão Repository

O padrão Repository é utilizado neste projeto para abstrair o acesso ao banco de dados, centralizando as operações CRUD (Create, Read, Update, Delete) e regras de validação em classes específicas. Isso facilita a manutenção, testes, reutilização e futuras migrações de banco de dados.

## Vantagens

- Desacoplamento entre lógica de negócio e persistência
- Facilita testes unitários (mock dos repositórios)
- Centraliza validações e regras de integridade
- Permite migração futura para outros bancos (ex: PostgreSQL)

## Estrutura no Projeto

- `app/core/repositories.py`: Repositórios específicos para cada entidade, com validações de negócio.
- `app/core/repository.py`: Implementação genérica e base para repositórios.
- `app/crud.py`: Funções CRUD refatoradas para usar os repositórios.

## Exemplo de Uso

```python
from app.core.database import SessionLocal
from app.core.repositories import MedicoRepository
from app.models.medico import Medico

with SessionLocal() as db:
    repo = MedicoRepository(db)
    medico = Medico(nome="Exemplo", crm="12345", especialidade_id=1)
    repo.create(medico)
    todos = repo.get_all()
```

## Testes

Os repositórios possuem testes unitários em `tests/unit/test_repositories.py`, cobrindo cenários de sucesso e erro.

## Referências

- [Martin Fowler - Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
