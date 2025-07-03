Roteiro de Desenvolvimento Incremental - GEM

1. Preparo do Ambiente

- [X] Criar o repositório no GitHub.
- [X] Criar ambiente virtual Python (venv).
  - [X] Escolha da IDE: VS Code
  - [X] Configuração do Ambiente Virtual
- [X] Gerar estrutura de pastas:
  - Escala/ (controllers, models, repositories, services, utils/logger.py)
  - app/ (views, assets, src, alembic, tests)
  - docs/, requirements.txt, README.md, main.py, cronograma_desenvolvimento.md

2. Configuração Básica

- [X] Instalar dependências principais (`PySide6`, `SQLAlchemy`, `alembic`, `pytest`, etc.).
- [X] Configurar logging centralizado em `Escala/utils/logger.py`.
- [X] Preparar script de inicialização (`main.py`) com janela principal vazia (front controller).



## 3. Modelagem do Banco e ORM

- [ ] Definir modelos iniciais (ORM – SQLAlchemy): `Medico`, `Especializacao`, `Escala`, `Usuario`, `AuditLog`.
- [ ] Configurar base do SQLAlchemy e conexão SQLite.
- [ ] Gerar e aplicar primeira migration com Alembic.
- [ ] Criar scripts de triggers/views se necessário (docs/sql/).
