# Guia de Implementação: Front Controller no Estilo Pablo Dall'Oglio (Adaptação Python)

Este documento detalha como implementar o padrão **Front Controller** na sua aplicação Python, seguindo o modelo apresentado por Pablo Dall'Oglio para PHP, porém adaptado ao contexto desktop/Python. Também mostra como organizar a estrutura de herança com o pattern **Layer Supertype** (classe base Page para todos os controllers), e como interligar com o Page Controller.

---

## 1. Estrutura Recomendada de Pastas

```
Lib/
  Escala/
    Core/
      class_loader.py
      app_loader.py
    Control/
      Page.py
app/
  Control/
    UsuarioControl.py
  Model/
    Usuario.py
  Templates/
    template.html
    assets/
main.py
```

---

## 2. Implementação da Superclasse Page (Layer Supertype)

Arquivo: `Lib/Escala/Control/Page.py`

```python
class Page:
    """
    Classe base para todos os Page Controllers.
    Fornece o método show(), que decide qual método executar baseado nos parâmetros recebidos.
    """

    def show(self, param=None):
        """
        Executa determinado método de acordo com os parâmetros recebidos (simulando $_GET em PHP).
        Se param for None, utiliza um método padrão (ex: listar).
        """
        if param is None:
            param = {}

        # Obtém o método a ser executado ('method' em param, ou 'listar' por padrão)
        method = param.get('method', 'listar')

        # Se existir o método, chama-o; senão, retorna mensagem de erro
        if hasattr(self, method) and callable(getattr(self, method)):
            return getattr(self, method)(param)
        else:
            return f"<h3>Método '{method}' não encontrado em {self.__class__.__name__}</h3>"
```

---

## 3. Exemplo de Controller Específico: UsuarioControl

Arquivo: `app/Control/UsuarioControl.py`

```python
from Lib.Escala.Control.Page import Page
from app.Model.Usuario import Usuario

class UsuarioControl(Page):
    def listar(self, param=None):
        try:
            usuarios = Usuario.all()
            html = "<h2>Lista de Usuários</h2><ul>"
            for usuario in usuarios:
                html += f"<li>{usuario.id} - {usuario.nome}</li>"
            html += "</ul>"
            return html
        except Exception as e:
            return f"<h3>Erro ao listar usuários: {e}</h3>"
```

---

## 4. Exemplo de Model: Usuario

Arquivo: `app/Model/Usuario.py`

```python
class Usuario:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def all():
        # Simula dados vindos do banco
        return [
            Usuario(1, "João"),
            Usuario(2, "Maria"),
            Usuario(3, "Carlos")
        ]
```

---

## 5. Ajuste no main.py (Front Controller)

Arquivo: `main.py`

```python
import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

from Lib.Escala.Core.class_loader import ClassLoader
from Lib.Escala.Core.app_loader import AppLoader

def load_template(path='app/Templates/template.html', context=None):
    context = context or {}
    with open(path, encoding='utf-8') as f:
        html = f.read()
    for key, value in context.items():
        html = html.replace('{' + key + '}', str(value))
    return html

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GEM - Gestão de Escala Médica")
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        self.show_page('UsuarioControl', {'method': 'listar'})
        self.showMaximized()

    def show_page(self, class_name, params=None):
        try:
            controller_cls = AppLoader.load_app_class(f"app.Control.{class_name}", class_name)
            controller = controller_cls()
            content = controller.show(params)  # show() da superclasse Page decide qual método chamar
        except Exception as e:
            content = f"<h2>Erro ao carregar página '{class_name}'</h2><pre>{e}</pre>"
        html = load_template(context={"content": content, "class": class_name})
        base_dir = os.path.abspath('app/Templates/')
        if not base_dir.endswith(os.sep):
            base_dir += os.sep
        self.browser.setHtml(html, baseUrl=QUrl.fromLocalFile(base_dir))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec()
```

---

## 6. Observações e Dicas

- Em um sistema web, os parâmetros viriam da URL (GET/POST). No desktop, podem vir de menus, botões, etc.
- O método `show_page` do MainWindow é o **Front Controller**: ele recebe a requisição (classe/método), instancia o controller e executa o método solicitado.
- Todos os seus controllers devem herdar de `Page` para garantir o controle centralizado de ações.
- Os Loaders (ClassLoader, AppLoader) garantem desacoplamento e flexibilidade, simulando o autoload do PHP de Pablo.

---

## 7. Resumo Visual do Fluxo

1. Usuário interage com o sistema (por exemplo, clica em "Listar Usuários")
2. O MainWindow (Front Controller) chama `show_page('UsuarioControl', {'method': 'listar'})`
3. AppLoader carrega dinamicamente a classe `UsuarioControl`
4. O método `show` da superclasse Page determina e executa o método correto (listar)
5. O resultado é renderizado na interface

---

## 8. Referências

- Pablo Dall'Oglio — "Frameworks para Desenvolvimento em PHP" (cap. 6)
- [Layer Supertype Pattern](https://martinfowler.com/eaaCatalog/layerSupertype.html)

---

**Recomenda-se seguir esta estrutura para garantir flexibilidade, reutilização e aderência aos padrões profissionais sugeridos por Pablo Dall'Oglio, mesmo em Python.**