# Algoritmo e Fluxo para Uso de Componentes na Aplicação (Exemplo com Usuário)

Este documento explica como utilizar e integrar **componentes** (widgets, elementos de UI) na arquitetura da aplicação, tomando como exemplo a entidade `Usuario`. O padrão seguido é inspirado nas práticas de Pablo Dall'Oglio, adaptadas para Python.

---

## 1. Estrutura dos Componentes

Os componentes reutilizáveis ficam organizados em:
```
Lib/
  Escala/
    Widgets/
      Base/
        element.py
      Form/
        form.py
        field.py
      ...
```
Cada componente é uma classe Python, podendo ser herdada e personalizada.

---

## 2. Exemplo de Componentes

### a) Componente Base (`Element`)
Arquivo: `Lib/Escala/Widgets/Base/element.py`
```python
class Element:
    def __init__(self, tag):
        self.tag = tag
        self.children = []
        self.attributes = {}

    def add(self, child):
        self.children.append(child)

    def set_attribute(self, key, value):
        self.attributes[key] = value

    def render(self):
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attributes.items())
        children = "".join(child.render() if hasattr(child, "render") else str(child) for child in self.children)
        return f"<{self.tag} {attrs}>{children}</{self.tag}>"
```

### b) Componente de Formulário (`Form`)
Arquivo: `Lib/Escala/Widgets/Form/form.py`
```python
from Lib.Escala.Widgets.Base.element import Element

class Form(Element):
    def __init__(self, name):
        super().__init__('form')
        self.set_attribute('name', name)

    def add_field(self, field):
        self.add(field)
```

### c) Componente de Campo (`Field`)
Arquivo: `Lib/Escala/Widgets/Form/field.py`
```python
from Lib.Escala.Widgets.Base.element import Element

class Field(Element):
    def __init__(self, name, field_type='text'):
        super().__init__('input')
        self.set_attribute('name', name)
        self.set_attribute('type', field_type)
```

---

## 3. Exemplo Real: Listando Usuários com Componente

### a) Model de Usuário
Arquivo: `app/Model/Usuario.py`
```python
class Usuario:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def all():
        return [
            Usuario(1, "João"),
            Usuario(2, "Maria"),
            Usuario(3, "Carlos")
        ]
```

### b) Controller usando um componente
Arquivo: `app/Control/UsuarioControl.py`
```python
from Lib.Escala.Control.Page import Page
from app.Model.Usuario import Usuario
from Lib.Escala.Widgets.Base.element import Element

class UsuarioControl(Page):
    def listar(self, param=None):
        usuarios = Usuario.all()
        lista = Element('ul')
        for usuario in usuarios:
            item = Element('li')
            item.add(f"{usuario.id} - {usuario.nome}")
            lista.add(item)
        return f"<h2>Lista de Usuários</h2>{lista.render()}"
```

---

## 4. Fluxo do Algoritmo

1. **Requisição do Usuário:**  
   O usuário solicita (via menu, botão ou URL) a listagem de usuários.

2. **Front Controller:**  
   O `main.py` interpreta a ação, identifica que deve chamar `UsuarioControl` e o método `listar`.

3. **Instancia o Controller:**  
   O controller é carregado dinamicamente pelo `AppLoader`.

4. **Uso do Componente:**  
   O método `listar` do controller utiliza o componente `Element` para montar a lista (`ul` e `li`).

5. **Renderização:**  
   O componente (`Element`) gera o HTML final usando seu método `render()`, retornando para o Front Controller.

6. **Exibição:**  
   O resultado é inserido no template e exibido ao usuário na interface.

---

## 5. Vantagens do Fluxo

- **Reutilização:** Qualquer controller pode usar os mesmos componentes.
- **Padronização:** Todos os elementos visuais seguem uma mesma interface (`render()`).
- **Desacoplamento:** O controller apenas instancia e usa componentes, não conhece detalhes de renderização final.
- **Facilidade de expansão:** Novos componentes podem ser adicionados em `/Lib/Escala/Widgets/` e usados imediatamente.

---

## 6. Resumo Visual

```
Usuário -> MainWindow (Front Controller) -> UsuarioControl (Page Controller) -> Componentes (Element, Form, Field) -> HTML -> Interface
```

---

**Dica:**  
Você pode criar componentes mais avançados (tabelas, grids, painéis, botões, etc.) seguindo essa mesma estrutura, sempre herdando de `Element` e implementando o método `render()`.
