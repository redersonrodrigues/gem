# Guia Rápido de Configuração – GEM

## 1. IDEs Recomendadas

- **PyCharm** (Community/Professional): Completo para Python.
- **VS Code** + Extensão Python: Leve, ótimo para PySide6 e notebooks.
- Outras: Visual Studio, Thonny, Spyder, Sublime Text.

## 2. Ambiente Virtual

Sempre use ambiente virtual para isolar dependências.

```sh
python -m venv .venv
# Ativação:
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

## 3. Instalação de Dependências

- As dependências estão em `requirements.txt`.
- Edite conforme necessário.

**Exemplo de dependências principais:**

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

_(Adicione outras conforme necessidade.)_

**Instalar tudo:**

```sh
pip install -r requirements.txt
```

**Adicionar nova dependência:**

```sh
pip install flask  # exemplo
pip freeze > requirements.txt
```

> Dica: Fixe versões em produção para garantir estabilidade (ex: `PySide6==6.7.0`).

## 4. Estrutura de Pastas do Projeto

A estrutura do projeto segue o padrão recomendado por Pablo Dall'Oglio para aplicações Python desktop modulares e reutilizáveis:

```
Lib/
    Escala/
        Control/        # Conterá classes que interpretarão ações e gerenciarão o fluxo de controle
        Core/           # Conterá classes que serão responsáveis pela carga das demais classes da aplicação
        Database/       # Conterá classes responsáveis pela Persistência de Dados
        Log/            # Conterá classes de log
        Session/        # Conterá classes de manipulação de sessões
        Traits/         # Conterá traits que poderão ser reaproveitados em diferentes contextos
        Validations/    # Conterá classes de validação de dados
        Widgets/        # Cnterá componentes utilizados para a montagem de interfaces, como formulários e datagrids

App/
    Config/            # Conterá arquivos de configuração da aplicação, tais como de acesso às bases de dados
    Control/           # Conterá classes de controle da aplicação
    Database/          # Eventualmente, conterá base de dados, como aquelas em SQLite
    Images/            # Conterá imagens específicas da aplicação
    Model/             # Conterá as classes de modelo da aplicação
    Resources/         # Conterá recursos externos com fragmentos de arquivos  (csv, txt, html, etc) utilizados na montagem de interfaces
    Services/          # Conterá classes que formam serviços, como aqueles voltados para web services
    Templates/         # Conterá os templates que formarão o layout da aplicação
    tests/             # Conterá os Testes automatizados da aplicação

docs/                  # Documentação do projeto
main.py                # Script principal (front controller)
requirements.txt       # Dependências do projeto
README.md              # Guia rápido e instruções
```

### 4.1 Resumo das Responsabilidades

- **Lib/Escala/**: Biblioteca reutilizável, framework, núcleo, controladores, modelos, repositórios, traits, widgets e utilitários genéricos. Tudo que pode ser aproveitado em outros projetos.
- **App/**: Código específico desta aplicação: controladores, modelos, serviços, recursos, imagens, templates, configurações e testes.
- **main.py**: Ponto de entrada da aplicação, inicializa o ambiente, carrega o núcleo do framework e exibe a janela principal.
- **docs/**: Documentação técnica e de usuário.

### 4.2 Exemplo de Fluxo (Front Controller)

O arquivo `main.py` faz a inicialização da aplicação e exibe a janela principal. Para um front controller real, importe o controlador principal de `Lib/Escala/Control` ou de `App/Control`:

```python
from PySide6.QtWidgets import QApplication
from Lib.Escala.Control.controllers import FrontController  # Exemplo
import sys

def main():
    app = QApplication(sys.argv)
    window = FrontController()  # Substitua por seu front controller real
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

Adapte o import conforme a implementação do seu controlador principal.

---

## 5. Logging Centralizado

O logger centralizado está em `Escala/utils/logger.py`. Importe e use em qualquer módulo:

```python
from Escala.utils.logger import get_logger
logger = get_logger(__name__)
```

Todos os logs vão para o console e para o arquivo `logs/gem_app.log`.

---

## Exemplo de Implementação do main.py

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from gem.Escala.Core.class_loader import ClassLoader
from gem.Escala.Core.app_loader import AppLoader
from gem.utils.logger import get_logger

logger = get_logger(__name__)

def load_template(path='app/Templates/template.html'):
    """
    Lê um template HTML, se for necessário para relatórios ou interface híbrida.
    Não é usado diretamente na janela principal Qt, mas pode ser útil para futuras funções.
    """
    try:
        with open(path, encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"Falha ao carregar template: {e}")
        return "<h1>Erro ao carregar template</h1>"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEM - Gestão de Escala Médica")
        self.setGeometry(100, 100, 900, 600)
        # Futuramente: adicionar widgets, menus, status bar, etc.

def main():
    logger.info("Iniciando aplicação GEM (Front Controller)...")
    app = QApplication(sys.argv)
    window = MainWindow()
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

### Resumo do funcionamento

- Utiliza os loaders (`ClassLoader`, `AppLoader`), prontos para expansão futura.
- Inicia a aplicação com uma janela principal vazia, título e tamanho definidos.
- Adota logging centralizado para rastreamento de eventos e erros.
- Estrutura pronta para evoluir conforme o padrão de Pablo Dall’Oglio, com Front Controller e organização modular.

### Como utilizar

1. Certifique-se de que as dependências estão instaladas (`pip install -r requirements.txt`).
2. Execute a aplicação com:
   ```sh
   python main.py
   ```
3. O logger registrará eventos no console e no arquivo de log.
4. Expanda a classe `MainWindow` e os loaders conforme a necessidade do seu projeto.

---

## 6. Templates e Componentes de Interface

### Templates (Layout Visual)

- Os arquivos de template HTML, CSS, JS e imagens estão localizados em `app/Templates/`.
- O arquivo principal é `template.html`, podendo ser utilizado para relatórios ou visualização híbrida.
- O método `load_template` em `main.py` permite carregar templates HTML para uso futuro, como geração de relatórios ou visualização web.

### Componentes de Interface (Widgets)

- Componentes reutilizáveis de interface ficam em `Lib/Escala/Widgets/`, organizados por tipo (Form, Datagrid, Dialog, Container, etc).
- Esses widgets são classes Python que facilitam a montagem de formulários, tabelas, diálogos e outros elementos de interface, seguindo o padrão modular.

### Separação de Responsabilidades

- O layout visual (HTML/CSS/JS) é mantido separado dos componentes de interface Python.
- Isso permite flexibilidade para evoluir tanto a interface gráfica (Qt) quanto relatórios ou visualizações web, mantendo o código organizado e reutilizável.

---

## 7. Como usar o sistema de template para exibir telas da aplicação

O sistema de template do GEM permite separar o layout visual do conteúdo dinâmico das telas, facilitando a manutenção e a evolução da interface.

### Estrutura

- O arquivo `app/Templates/template.html` contém o layout base, com um container central:
  ```html
  <div id="content-area">{content}</div>
  ```
- O marcador `{content}` é substituído pelo Python pelo conteúdo HTML da tela desejada.
- O menu Qt (criado no Python) controla a navegação entre as telas.
- O componente `QWebEngineView` exibe o template, aplicando todo o CSS/JS.

### Como exibir o conteúdo das telas

1. **Defina o conteúdo HTML de cada tela**
   - No Python, crie strings HTML para cada tela (exemplo: `<h2>Cadastro de Médicos</h2>`, formulários, tabelas, etc).
   - No método `show_in_template` da classe `MainWindow`, associe cada item do menu ao HTML correspondente usando um dicionário:
     ```python
     content_map = {
         "medicos": "<h2>Cadastro e Gestão de Médicos</h2>",
         "escalas": "<h2>Cadastro e Gestão de Escalas</h2>",
         # ... outros itens ...
     }
     ```
2. **Atualize o conteúdo dinamicamente**
   - Ao clicar em um item do menu, o método `show_in_template` executa um JavaScript no template:
     ```python
     js = f"setContent(`{html_content}`);"
     self.browser.page().runJavaScript(js)
     ```
   - Isso troca apenas o conteúdo do container, sem recarregar a página inteira.

### Vantagens

- Separação total entre layout (HTML/CSS/JS) e lógica de navegação (Python/Qt).
- Facilidade para criar, modificar ou reaproveitar telas.
- Interface estilizada e responsiva, aproveitando todo o poder do template HTML.
- Navegação controlada pelo menu Qt, mantendo o padrão desktop e a arquitetura modular.
