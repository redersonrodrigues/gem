# Documentação do Componente Element

Este documento descreve a implementação e o uso do componente `Element` para construção de tags HTML de forma orientada a objetos, no padrão inspirado por Pablo Dall'Oglio.

---

## 1. Objetivo

O componente `Element` permite criar, manipular e exibir elementos HTML (como `<div>`, `<p>`, `<img>`, etc.) usando programação orientada a objetos em Python.  
Ele facilita a criação de componentes reutilizáveis e a construção dinâmica da interface, isolando propriedades e filhos de cada elemento.

---

## 2. Implementação

### Arquivo: `Lib/Escala/Widgets/Base/element.py`

```python
class Element:
    """
    Classe suporte para tags HTML (p, img, div, etc.), no padrão de Pablo Dall'Oglio.
    Permite adicionar propriedades e filhos, e exibe o HTML correspondente.
    """

    def __init__(self, tagname):
        self.tagname = tagname         # nome da tag
        self._properties = {}          # propriedades do elemento/tag
        self.children = []             # filhos, que podem ser outros elementos ou strings

    def __setattr__(self, name, value):
        # Intercepta atribuições de propriedades dinâmicas (exceto atributos internos)
        if name in ('tagname', '_properties', 'children'):
            super().__setattr__(name, value)
        else:
            self._properties[name] = value

    def __getattr__(self, name):
        # Retorna atributos do dicionário de propriedades, se existirem
        if name in self._properties:
            return self._properties[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def add(self, child):
        """
        Adiciona um elemento filho (objeto ou string)
        """
        self.children.append(child)

    def open(self):
        """
        Exibe a tag de abertura com propriedades
        """
        props = ''
        for name, value in self._properties.items():
            if isinstance(value, (str, int, float, bool)):
                props += f' {name}="{value}"'
        print(f"<{self.tagname}{props}>", end='')

    def close(self):
        """
        Exibe a tag de fechamento
        """
        print(f"</{self.tagname}>")

    def show(self):
        """
        Exibe a tag na tela, junto com seus filhos
        """
        self.open()
        print()  # Nova linha após a abertura da tag

        for child in self.children:
            if hasattr(child, 'show'):
                child.show()
            else:
                print(child, end='')

        self.close()
        print()  # Nova linha após fechamento

    def __str__(self):
        """
        Converte o elemento para string (útil para print(obj))
        """
        from io import StringIO
        import sys

        # Redireciona o print para buffer
        buffer = StringIO()
        stdout = sys.stdout
        sys.stdout = buffer
        self.show()
        sys.stdout = stdout
        return buffer.getvalue()
```

---

## 3. Exemplo de Uso

### Arquivo: `app/Control/ExemploElementControl.py`

```python
from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Base.element import Element

class ExemploElementControl(Page):
    def __init__(self):
        super().__init__()

        div = Element('div')
        div.style = 'text-align:center; font-weight:bold; font-size:14pt; margin:20px;'

        p = Element('p')
        p.add('Isto é um teste de parágrafo')

        div.add(p)

        self.add(div)
```

### Exibindo na tela

No seu Front Controller ou teste, faça:

```python
ctrl = ExemploElementControl()
print(ctrl.show())
```

Isso irá imprimir o HTML equivalente a:

```html
<div style="text-align:center; font-weight:bold; font-size:14pt; margin:20px;">
<p>
Isto é um teste de parágrafo</p>
</div>
```

---

## 4. Vantagens

- Permite construir componentes HTML de forma orientada a objetos.
- Facilita reutilização e composição de widgets.
- Propriedades e filhos são gerenciados de forma flexível.
- Integrável com padrões maiores, como Template View e Page Controller.

---

## 5. Observações

- O método `add()` pode receber tanto strings quanto outros objetos `Element`.
- Os atributos HTML devem ser definidos como propriedades do objeto após a criação (ex: `obj.style = "..."`).
- O método `show()` imprime o HTML na tela; o método `__str__()` permite obter o HTML como string.

---

**Resumo:**  
O componente `Element` é essencial para criar componentes visuais reutilizáveis e flexíveis, promovendo a separação da lógica e da apresentação no desenvolvimento de sistemas Python com inspiração em padrões do Livro do Pablo Dall'Oglio.