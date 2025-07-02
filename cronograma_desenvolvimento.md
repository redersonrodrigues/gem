Roteiro de Desenvolvimento Incremental - GEM

1. Preparo do Ambiente

- [x] Criar o repositório no GitHub.
- [x] Criar ambiente virtual Python (venv).
  - [x] Escolha da IDE: VS Code
  - [x] Configuração do Ambiente Virtual
- [x] Gerar estrutura de pastas:
  - Escala/ (controllers, models, repositories, services, utils/logger.py)
  - app/ (views, assets, src, alembic, tests)
  - docs/, requirements.txt, README.md, main.py, cronograma_desenvolvimento.md

2. Configuração Básica

- [x] Instalar dependências principais (`PySide6`, `SQLAlchemy`, `alembic`, `pytest`, etc.).
- [x] Configurar logging centralizado em `Escala/utils/logger.py`.
- [x] Preparar script de inicialização (`main.py`) com janela principal vazia (front controller).

## 3. Modelagem do Banco e ORM

- [ ] Definir modelos iniciais (ORM – SQLAlchemy): `Medico`, `Especializacao`, `Escala`, `Usuario`, `AuditLog`.
- [ ] Configurar base do SQLAlchemy e conexão SQLite.
- [ ] Gerar e aplicar primeira migration com Alembic.
- [ ] Criar scripts de triggers/views se necessário (docs/sql/).
