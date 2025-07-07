# Guia Rápido de Configuração – GEM (Desktop PySide6)

## 1. IDEs Recomendadas

- **PyCharm** (Community/Professional): Ótima para grandes projetos Python.
- **VS Code** + Extensão Python: Leve, rápido, excelente para PySide6.
- Outras: Visual Studio, Thonny, Spyder, Sublime Text.

---

## 2. Ambiente Virtual

Sempre use um ambiente virtual para isolar dependências.

```sh
python -m venv .venv
# Ativação:
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

---

## 3. Instalação de Dependências

- As dependências estão em `requirements.txt`.
- Edite conforme necessário para seu ambiente.

**Principais dependências:**

```
PySide6
qtawesome
SQLAlchemy
alembic
passlib
bcrypt
cryptography
pytest
pytest-qt
pytest-cov
pytest-benchmark
loguru
matplotlib
seaborn
pyqtgraph
pandas
black
isort
```

**Para instalar tudo:**

```sh
pip install -r requirements.txt
```

**Para adicionar nova dependência:**

```sh
pip install <nome-do-pacote>
pip freeze > requirements.txt
```

> **Dica:** Fixe as versões em produção para garantir estabilidade (ex: `PySide6==6.7.0`).

---

## 4. Estrutura de Pastas do Projeto

O projeto GEM segue a organização modular inspirada nos padrões do Pablo Dall'Oglio, adaptada para aplicações desktop em PySide6:

```
Lib/
    Escala/
        Control/        # Controladores e Front Controller (navegação e lógica geral)
        Core/           # Autoloaders e núcleo do framework
        Database/       # Persistência de dados e ORM
        Log/            # Centralização de logs
        Session/        # Manipulação de sessão (se aplicável)
        Traits/         # Traits reutilizáveis em diferentes contextos
        Validations/    # Validações de dados
        Widgets/        # Componentes PySide6 reutilizáveis (Painéis, Caixa de Mensagem, Diálogos, etc.)

App/
    Config/            # Configurações da aplicação (banco, chaves, etc.)
    Control/           # Controladores específicos da aplicação (telas/pages)
    Database/          # Bases de dados locais (ex: SQLite)
    Images/            # Imagens específicas da aplicação
    Model/             # Modelos de domínio/entidades
    Resources/         # Recursos externos (csv, txt, html, etc)
    Services/          # Serviços, integrações externas, web services
    Templates/         # Templates para relatórios (usados por TemplateEngine)
    tests/             # Testes automatizados

docs/                  # Documentação do projeto
main.py                # Script principal (front controller)
requirements.txt       # Dependências do projeto
README.md              # Este guia
```

### 4.1 Resumo das Responsabilidades

- **Lib/Escala/**: Núcleo reutilizável (framework, widgets, utilitários, ORM, autoloaders, etc).
- **App/**: Código específico do GEM (controladores, modelos, recursos, templates, etc).
- **main.py**: Ponto de entrada da aplicação. Inicializa o front controller e a janela principal.
- **docs/**: Documentação técnica e de usuário.

---

## 5. Inicialização e Front Controller

O arquivo `main.py` faz a inicialização da aplicação, cria o ambiente e exibe a janela principal. O padrão Front Controller é aplicado com navegação controlada via widgets PySide6.

**Exemplo mínimo de `main.py`:**

```python
import sys
from PySide6.QtWidgets import QApplication
from Lib.Escala.Control.front_controller import FrontController  # Exemplo
from Lib.Escala.Core.class_loader import ClassLoader
from Lib.Escala.Core.app_loader import AppLoader
from Lib.Escala.Log.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Iniciando aplicação GEM Desktop (Front Controller)...")
    app = QApplication(sys.argv)
    window = FrontController()  # Substitua pelo seu front controller real
    window.show()
    try:
        ret = app.exec()
        logger.info("Aplicação encerrada normalmente.")
        sys.exit(ret)
    except Exception as e:
        logger.error(f"Erro fatal na aplicação: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

> **Adapte o import do FrontController conforme sua implementação real.**

---

## 6. Logging Centralizado

O logger centralizado está em `Lib/Escala/Log/logger.py`. Use em qualquer módulo:

```python
from Lib.Escala.Log.logger import get_logger
logger = get_logger(__name__)
```

Todos os logs vão para o console e para o arquivo `logs/gem_app.log`.

---

## 7. Componentes de Interface (Widgets)

- Componentes PySide6 reutilizáveis ficam em `Lib/Escala/Widgets/`, como:

  - **VBox, HBox**: Containers verticais e horizontais.
  - **Panel**: Painéis agrupadores com título.
  - **Message**: Mensagens informativas ou de erro.
  - **Question**: Diálogos de confirmação.
  - Outros: Formulários, datagrids, etc.
- Siga sempre o padrão modular e reutilizável.
- **Não há mais uso de HTML/Bootstrap na interface.**
  Todo o visual é feito com widgets Qt e, se necessário, estilização via `setStyleSheet()`.

---

## 8. Templates e Relatórios

8.1. **Templates para Relatórios, Documentos e Impressão**

- Os arquivos HTML (e eventualmente CSS) em `App/Templates/` **não servem mais para a interface principal** (menus, formulários, navegação), mas continuam sendo **muito úteis para geração de relatórios, impressão e documentos** (ex: escala médica impressa, recibos, comprovantes, PDFs).
- O **TemplateEngine** (ex: Jinja2, string.Template, ou até renderização manual) é usado para gerar o HTML do relatório/documento, preenchendo os dados dinâmicos.

**Exemplo de uso:**

```python
from jinja2 import Template

with open("App/Templates/escala.html") as f:
    template = Template(f.read())
html = template.render(medicos=lista_medicos, data="06/07/2025")
```

---

## 8.2. **Exibição dos Relatórios**

- **QWebEngineView** é o widget do Qt que permite exibir HTML (com ou sem CSS/JS) dentro da aplicação desktop.
- Você pode passar o HTML gerado dinamicamente para o widget, e o usuário visualiza, imprime ou exporta como PDF.

**Exemplo básico:**

```python
from PySide6.QtWebEngineWidgets import QWebEngineView

view = QWebEngineView()
view.setHtml(html)  # html é a string gerada pelo TemplateEngine
view.show()
```

---

## 8.3. **Impressão**

- O usuário pode imprimir diretamente pela interface do QWebEngineView (atalho Ctrl+P, botão ou menu).
- Se precisar de PDF, o PySide6 permite exportar a visualização para PDF facilmente.

**Exemplo de exportação para PDF:**

```python
def exportar_pdf(view: QWebEngineView, filename: str):
    view.page().printToPdf(filename)
```

---

## 8.4. **Resumo da Estratégia**

- **Interface principal**: 100% widgets Qt/PySide6 (QWidget, QMainWindow, QDialog, etc).
- **Templates HTML**: Usados **apenas** para relatórios/documentos que serão visualizados no QWebEngineView, impressos ou exportados.
- **Geração de relatórios**: Use TemplateEngine para gerar o HTML, passe para o QWebEngineView.
- **Impressão/Exportação**: O usuário pode imprimir ou exportar para PDF usando recursos do Qt.

---

## **Exemplo de Fluxo Completo**

1. O usuário clica “Imprimir Escala”.
2. O sistema gera o HTML do relatório usando um template em `App/Templates/`.
3. O HTML é exibido em um QWebEngineView dentro de um diálogo/modal.
4. O usuário pode visualizar, imprimir ou exportar o resultado.

---

## **Vantagens**

- Visualização rica e formatada de relatórios, sem misturar HTML com interface principal.
- Separação clara entre lógica de interface (Qt) e lógica de geração de documento (TemplateEngine).
- Fácil manutenção e atualização dos layouts de relatórios.

---

Se quiser um exemplo de código para todo esse fluxo (template → HTML → QWebEngineView → impressão), é só pedir!

---

## 9. Testes

- Testes automatizados ficam em `App/tests/`.
- Use `pytest`, `pytest-qt` e outros utilitários citados em `requirements.txt`.

---

## 10. Expansão e Organização

- Adicione novos widgets, controladores, modelos e recursos seguindo a estrutura modular.
- Use os autoloaders (`ClassLoader`, `AppLoader`) para carregar componentes dinamicamente.
- Mantenha a separação entre código genérico (reutilizável) e código específico da aplicação.

---

## 11. Dúvidas, Contribuições e Documentação

- Consulte a pasta `docs/` para documentação técnica, diagramas e guias de uso.
- Para dúvidas ou sugestões, abra issues ou contribua com pull requests.

---

## 12. Resumo

- **GEM Desktop** é uma aplicação modular, reutilizável e expansível para gestão de escala médica.
- Segue os padrões Page Controller, Front Controller e Template View.
- 100% interface Qt/PySide6.
- Padrão de organização inspirado em Pablo Dall’Oglio, adaptado para desktop.
- Documentação e exemplos disponíveis na pasta `docs/`.

---
