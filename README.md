# GEM - Gestão de Escalas Médicas

[![GitHub](https://img.shields.io/badge/GitHub-gem-blue?logo=github)](https://github.com/seu-usuario/gem)
[![Build Status](https://github.com/seu-usuario/gem/actions/workflows/ci.yml/badge.svg)](https://github.com/seu-usuario/gem/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Setup Inicial](#setup-inicial)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)
- [Roadmap](#roadmap)
- [Ambiente](#ambiente)
- [Documentação](#documentação)
- [Contribuição](#contribuição)
- [Segurança](#segurança)
- [Suporte](#suporte)
- [Licença](#licença)

## Visão Geral

Aplicação desktop para gestão de escalas médicas (plantonistas e sobreaviso), desenvolvida em Python, arquitetura MVC, com foco em qualidade, segurança, usabilidade e integração.

## Funcionalidades

- Cadastro e gestão de médicos, especializações e escalas
- Interface gráfica responsiva (PyQt5)
- Modo claro/escuro com comutador
- Relatórios e exportação em PDF (ReportLab, PyPDF2)
- Testes automatizados (pytest, pytest-cov, pytest-qt)
- Integração com banco SQLite (SQLAlchemy)
- Controle de acesso e permissões (admin/usuário)
- Geração de logs e auditoria
- Integração futura com APIs externas
- Layout adaptado para diferentes tamanhos de tela
- Uso local de ícones FontAwesome

## Setup Inicial

1. Crie e ative o ambiente virtual Python:

   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie o arquivo `.env.example` para `.env` e configure as variáveis sensíveis (se necessário).

4. Execute a aplicação:

   ```bash
   python main.py
   ```

## Estrutura do Projeto

- app/: Código principal (MVC, models, views, controllers)
- static/: Arquivos estáticos (ícones, css, imagens)
- tests/: Testes automatizados
- scripts/: Scripts auxiliares e SQL
- docs/: Documentação técnica (consulte `docs/` para detalhes, diagramas e guias)
- todo.todo: Checklist detalhado do projeto

## Testes

- Para rodar todos os testes:

  ```bash
  pytest
  ```

- Para gerar relatório de cobertura:

  ```bash
  pytest --cov=app
  ```

- Para testar interface gráfica:

  ```bash
  pytest --qt-log-level=INFO
  ```

## Roadmap

- [x] Estrutura inicial, ambiente, dependências, CI/CD
- [x] README, LICENSE, CONTRIBUTING.md
- [x] Estrutura de documentação e setup
- [ ] Modelagem do banco de dados e scripts SQL
- [ ] Implementação dos modelos e repositórios
- [ ] CRUDs, regras de negócio e interface gráfica
- [ ] Controle de acesso, logs, relatórios e integrações
- [ ] Testes completos e cobertura
- [ ] Otimizações, segurança, deploy e melhorias contínuas

## Ambiente

- Python 3.8+ (recomendado: 3.13)
- Testado em Windows 10/11
- Requer VSCode ou editor compatível

## Principais Tecnologias

- Python 3.8+
- PyQt5 (interface gráfica)
- SQLAlchemy (ORM)
- SQLite (banco de dados local)
- Flask (API e backend)
- pytest, pytest-cov, pytest-qt (testes)
- ReportLab, PyPDF2 (relatórios e PDFs)

## Documentação

A documentação técnica detalhada está disponível na pasta `docs/`.

## Segurança

- Variáveis sensíveis em `.env` (não versionado)
- Uso de boas práticas PEP8/PEP257
- Estrutura para controle de acesso, logs e auditoria
- Planejamento para criptografia de dados sensíveis

## Suporte

- Para dúvidas, sugestões ou reporte de bugs, abra uma issue no GitHub ou envie e-mail para: [contato@seudominio.com](mailto:contato@seudominio.com)

## Contribuição

Consulte o arquivo CONTRIBUTING.md para diretrizes de contribuição.

## Screenshots

<!-- Adicione imagens reais da interface quando disponível -->

![Tela principal](static/assets/demo1.png)
![Cadastro de médico](static/assets/demo2.png)

## Licença

Este projeto está licenciado sob os termos da licença MIT.

[Repositório no GitHub](https://github.com/seu-usuario/gem)

## Padrão Repository

O projeto utiliza o padrão Repository para abstrair o acesso ao banco de dados, centralizando operações CRUD e regras de validação em classes específicas. Isso facilita manutenção, testes e futuras migrações de banco.

- Implementação genérica: `app/core/repository.py`
- Repositórios específicos: `app/core/repositories.py`
- Funções CRUD refatoradas: `app/crud.py`
- Testes: `tests/unit/test_repositories.py`
- Documentação detalhada: [`docs/repository.md`](docs/repository.md)

## Padrão Dinâmico de Caminho do Banco de Dados (SQLite)

Toda a aplicação, scripts e testes suportam o uso dinâmico do caminho do banco de dados SQLite.

- O core (`app/core/database.py`) permite informar o caminho do banco via argumento `db_path` em todas as funções principais.
- Todos os scripts aceitam o argumento `--db-path` para operar sobre qualquer arquivo de banco.
- Os testes automatizados utilizam bancos temporários, garantindo isolamento.
- O padrão é retrocompatível: se não informado, utiliza `gem.db` na raiz do projeto.
- Consulte a documentação detalhada em [`docs/sql/padrao_db_dinamico.md`](docs/sql/padrao_db_dinamico.md).

**Exemplo de uso em script:**

```sh
python scripts/export_db.py --db-path tests/tmp/teste.db
```

**Exemplo de uso no core:**

```python
from app.core.database import get_engine, init_db
engine = get_engine(db_path='tests/tmp/teste.db')
init_db(db_path='tests/tmp/teste.db')
```

## Banco de Dados: SQLite (desenvolvimento) e PostgreSQL (produção)

- O backend suporta tanto SQLite (padrão, para desenvolvimento/testes) quanto PostgreSQL (recomendado para produção).
- Para produção, configure a string de conexão PostgreSQL conforme exemplo:

  ```text
  postgresql+psycopg2://usuario:senha@localhost:5432/gem
  ```

- Instale o driver com:

  ```bash
  pip install psycopg2-binary
  ```

- Veja instruções detalhadas e recomendações em `docs/sql/postgresql_producao.md`.

## Migração de Dados entre Ambientes

O projeto possui um script dedicado para migração de dados entre bancos de diferentes ambientes (desenvolvimento, teste, produção), suportando SQLite e PostgreSQL.

- Script: `scripts/migrate_db.py`
- Permite migrar todas as tabelas ou apenas selecionadas.
- Suporta caminhos/URLs dinâmicos de banco.
- Testado com bancos temporários e integração automatizada.
- Documentação detalhada: [`docs/sql/migracao_dados.md`](docs/sql/migracao_dados.md)

**Exemplo de uso:**

```sh
python scripts/migrate_db.py --src-db gem_dev.db --dst-db gem_prod.db --tables medicos,especializacoes
```

> Recomendações: sempre faça backup antes de migrar e valide os dados após a operação.
