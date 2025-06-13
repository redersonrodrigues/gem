# GEM - Gestão de Escalas Médicas

## Descrição
O GEM é um sistema para gestão de escalas médicas, cadastro de profissionais, especializações e relatórios, desenvolvido em Python com Flask, SQLite, SQLAlchemy, Bootstrap e PyQt5. O sistema é multiplataforma, responsivo e pode ser executado localmente, sem necessidade de internet.

## Funcionalidades
- Cadastro e gerenciamento de médicos, especializações e escalas
- Relacionamento muitos-para-muitos entre médicos e especializações
- Escalas de plantonistas (turnos de 12h, dois médicos por turno, registro único por dia)
- Escalas de sobreaviso ortopedia (quinzenal) e demais especialidades (semanal)
- Layout responsivo, modo claro/escuro, padronização visual
- Testes automatizados com pytest
- Documentação técnica com Sphinx

## Instalação e Execução
1. Clone o repositório:
   ```powershell
   git clone <url-do-repositorio>
   cd gem
   ```
2. Crie e ative o ambiente virtual:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate
   ```
3. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
4. Popule as especializações iniciais:
   ```powershell
   python -m app.models.populate_specializations
   ```
5. Execute a aplicação:
   ```powershell
   python main.py
   ```
6. Execute os testes:
   ```powershell
   python -m pytest
   ```

## Estrutura do Projeto
- `app/` - Código principal (modelos, controladores, views)
- `static/` - Arquivos estáticos (css, js, imagens, bootstrap, fontawesome)
- `templates/` - Templates Jinja2
- `tests/` - Testes automatizados
- `docs/` - Documentação técnica
- `main.py` - Inicialização do Flask
- `requirements.txt` - Dependências
- `.todo` - Checklist de tarefas do projeto

## Melhorias, Funcionamentos e Ajustes
- [ ] A cada nova funcionalidade ou ajuste, documentar aqui o que foi feito, por que e como utilizar.
- [ ] Manter o checklist `.todo` atualizado, marcando tarefas concluídas e revisando sempre que necessário.

## Contribuição
- Siga as boas práticas de versionamento (commits claros e frequentes)
- Atualize o checklist `.todo` e este README.md a cada etapa
- Documente código e funcionalidades

---

*Este arquivo será atualizado continuamente conforme o desenvolvimento do projeto.*