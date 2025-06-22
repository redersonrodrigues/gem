# Migração de Dados entre Ambientes

Este documento descreve o procedimento e o script para migrar dados entre bancos de diferentes ambientes (desenvolvimento, teste, produção), suportando SQLite e PostgreSQL.

## Script de Migração

O script `scripts/migrate_db.py` permite migrar dados de tabelas selecionadas ou de todo o banco entre dois arquivos SQLite ou URLs de banco PostgreSQL.

### Uso

```bash
python migrate_db.py --src-db <caminho_ou_url_origem> --dst-db <caminho_ou_url_destino> [--tables tabela1,tabela2,...]
```

- `--src-db`: Caminho do banco de origem (ex: `gem_dev.db` ou `sqlite:///gem_dev.db` ou `postgresql://...`)
- `--dst-db`: Caminho do banco de destino (ex: `gem_prod.db` ou `sqlite:///gem_prod.db` ou `postgresql://...`)
- `--tables`: (Opcional) Lista de tabelas a migrar, separadas por vírgula. Se omitido, migra todas as tabelas.

### Exemplo

```bash
python migrate_db.py --src-db gem_dev.db --dst-db gem_prod.db --tables medicos,especializacoes
```

### Recomendações

- Sempre faça backup dos bancos antes de migrar.
- Garanta que os esquemas estejam compatíveis (mesmas tabelas e campos).
- Use o script em ambiente controlado e valide os dados após a migração.

### Limitações

- O script não migra constraints, triggers ou views, apenas dados das tabelas.
- Para migração de estrutura, use Alembic ou scripts SQL.

---

Documentação atualizada em 21/06/2025.
