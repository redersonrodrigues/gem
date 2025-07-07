# Arquitetura de Aplicação Desktop com PySide6
## Padrão Inspirado em Pablo Dall’Oglio

Este documento descreve a implementação de uma arquitetura desktop em **PySide6**, baseada nos padrões e raciocínios de Pablo Dall’Oglio (Livro do Programador), mas adaptada ao universo de widgets Qt, sem uso de HTML ou Bootstrap. A estrutura segue os conceitos de **Front Controller**, **Page Controller**, **Template View** e componentes reutilizáveis, com carregamento automático de classes via autoloaders.

---

## Índice

1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Front Controller (`MainWindow` e Navegação)](#front-controller)
3. [Page Controllers (Telas)](#page-controllers)
4. [Componentes Reutilizáveis (Widgets)](#componentes-reutilizáveis)
    - VBox
    - HBox
    - Panel
    - Message
    - Question
    - Action
5. [Template View (Visualização Padrão)](#template-view)
6. [Autoloaders (`app_loader` e `class_loader`)](#autoloaders)
7. [Fluxo de Execução](#fluxo-de-execução)
8. [Exemplo Completo de Uso](#exemplo-completo)
9. [Customização de Estilos](#customização-de-estilos)
10. [Conclusão](#conclusão)

---

## Visão Geral da Arquitetura

O objetivo é criar um sistema organizado, desacoplado e altamente reaproveitável, onde:

- Cada tela é representada por uma classe (Page Controller).
- Um controlador central (Front Controller) gerencia a navegação entre telas.
- Componentes são widgets reutilizáveis, componíveis e padronizados.
- O template view permite separar lógica de apresentação.
- Actions encapsulam comandos, facilitando callbacks e passagem de parâmetros.

---

## Front Controller

### O que é

No contexto desktop, o **Front Controller** é a janela principal (`MainWindow`) que gerencia qual tela (Page Controller) está visível, centralizando a navegação e a orquestração do fluxo da aplicação.

### Implementação

```python
from PySide6.QtWidgets import QMainWindow, QStackedWidget

class AppController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.show_page(HomePage)

    def show_page(self, page_class, *args, **kwargs):
        # Remove widgets antigos se necessário
        for i in range(self.stacked.count()):
            self.stacked.removeWidget(self.stacked.widget(i))
        # Instancia e exibe nova página
        page = page_class(self, *args, **kwargs)
        self.stacked.addWidget(page)
        self.stacked.setCurrentWidget(page)
```

- `show_page` centraliza qual página está visível na aplicação.
- Cada página recebe como primeiro argumento o controlador, facilitando navegação reversa.

---

## Page Controllers

### O que é

Cada tela (ou página) tem sua própria classe, responsável pela montagem dos widgets, layouts e lógica daquela tela.

### Implementação Exemplo

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class HomePage(QWidget):
    def __init__(self, app_controller):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Bem-vindo!"))
        btn = QPushButton("Ir para Clientes")
        btn.clicked.connect(lambda: app_controller.show_page(ClienteListPage))
        layout.addWidget(btn)
```

- O `app_controller` permite que a página solicite a navegação.
- O layout é montado no construtor, compondo widgets reutilizáveis.

---

## Componentes Reutilizáveis

Os componentes são widgets PySide6, inspirados na lógica dos componentes HTML do Pablo Dall’Oglio, mas usando widgets Qt nativos.

### 1. VBox

Empacota widgets verticalmente:

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout

class VBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def add(self, widget):
        self.layout.addWidget(widget)
```

---

### 2. HBox

Empacota widgets horizontalmente:

```python
from PySide6.QtWidgets import QWidget, QHBoxLayout

class HBox(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.setLayout(self.layout)

    def add(self, widget):
        self.layout.addWidget(widget)
```

---

### 3. Panel

Agrupa widgets com um título, igual ao `Panel` do Bootstrap:

```python
from PySide6.QtWidgets import QGroupBox, QVBoxLayout

class Panel(QGroupBox):
    def __init__(self, title=None, parent=None):
        super().__init__(title if title else "", parent)
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

    def add(self, widget):
        self.layout.addWidget(widget)
```

---

### 4. Message

Exibe uma mensagem com estilo customizável:

```python
from PySide6.QtWidgets import QLabel

class Message(QLabel):
    def __init__(self, type_, message, parent=None):
        super().__init__(message, parent)
        if type_ == "info":
            self.setStyleSheet("color: blue; background: #e7f3fe; border: 1px solid #b3d7ff; padding: 8px;")
        elif type_ == "error":
            self.setStyleSheet("color: red; background: #fdecea; border: 1px solid #f5c6cb; padding: 8px;")
        else:
            self.setStyleSheet("padding: 8px;")
```

---

### 5. Question (Diálogo de confirmação)

Dialog customizado para perguntas ao usuário, com ações para sim/não.

```python
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

class Question(QDialog):
    def __init__(self, message, action_yes, action_no=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pergunta")
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(message))

        btn_layout = QHBoxLayout()
        btn_yes = QPushButton("Sim")
        btn_yes.clicked.connect(lambda: self._do_action(action_yes))
        btn_layout.addWidget(btn_yes)

        if action_no:
            btn_no = QPushButton("Não")
            btn_no.clicked.connect(lambda: self._do_action(action_no))
            btn_layout.addWidget(btn_no)

        layout.addLayout(btn_layout)

    def _do_action(self, action):
        if action:
            action.execute()
        self.accept()
```

---

### 6. Action

Encapsula um comando a ser executado, com ou sem parâmetros (substitui o conceito de URL):

```python
class Action:
    def __init__(self, func, **params):
        self.func = func
        self.params = params

    def execute(self):
        self.func(**self.params)
```

---

## Template View

Permite criar uma visualização padronizada de dados, separando lógica de apresentação. Exemplo para um “card” de cliente:

```python
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

def cliente_card(cliente):
    w = QWidget()
    layout = QVBoxLayout(w)
    layout.addWidget(QLabel(f"Nome: {cliente['nome']}"))
    layout.addWidget(QLabel(f"Email: {cliente['email']}"))
    return w

# Uso em uma Page:
for cli in clientes:
    self.layout.addWidget(cliente_card(cli))
```

---

## Autoloaders (`app_loader` e `class_loader`)

- **app_loader**: Carrega automaticamente os módulos de controladores (pages) conforme solicitado pelo Front Controller.
- **class_loader**: Carrega componentes e widgets sob demanda, evitando imports manuais repetitivos.

**Exemplo de uso:**
```python
# app_loader.py
import importlib

def load_page(page_name):
    module = importlib.import_module(f'app.pages.{page_name}')
    return getattr(module, page_name)
```

---

## Fluxo de Execução

1. O usuário executa a aplicação.
2. O `AppController` (Front Controller) instancia e mostra a tela inicial (Page Controller).
3. O usuário interage com botões/menus, que disparam Actions.
4. O AppController instancia e mostra a próxima Page (Page Controller), conforme solicitado.
5. Componentes (VBox, Panel, Message, etc.) são utilizados na composição das páginas.
6. Diálogos de confirmação (Question) aparecem quando necessário, acionando Actions.
7. Template Views são usados para mostrar listas, cards e visualizações padronizadas.

---

## Exemplo Completo

```python
from PySide6.QtWidgets import QApplication
# Importe os componentes conforme seus arquivos

def on_confirma():
    print("Confirmado!")

def on_nega():
    print("Negado!")

app = QApplication([])

main = VBox()
panel = Panel("Painel de Mensagem")
panel.add(Message("info", "Bem-vindo ao sistema!"))
panel.add(Message("error", "Erro de teste"))
main.add(panel)

action_yes = Action(on_confirma)
action_no = Action(on_nega)
question = Question("Deseja confirmar esta operação?", action_yes, action_no)
question.exec()

main.show()
app.exec()
```

---

## Customização de Estilos

- Use `.setStyleSheet()` nos widgets para customizar cores, bordas e espaçamento.
- Qt suporta temas (Fusion, Windows, etc.) e integração com o tema do sistema operacional.

---

## Conclusão

- Esta arquitetura permite **fácil manutenção**, **componentização** e **expansão** da aplicação desktop.
- O padrão de organização inspirado em Pablo Dall’Oglio é plenamente aplicável ao Qt/PySide6, bastando adaptar a camada visual para widgets nativos.
- Actions, Pages, Templates e Front Controller continuam sendo ferramentas poderosas para separação de responsabilidades.
- Os autoloaders facilitam a modularização e a organização do projeto.

Se desejar exemplos mais avançados (CRUD, integração com banco de dados, etc.), basta pedir!
