# Documentação do Componente Panel (Painel)

Este documento descreve a implementação e o uso do componente `Panel` (Painel), inspirado no padrão de Pablo Dall'Oglio, para delimitar áreas com bordas e título na interface, utilizando classes de estilo do Bootstrap.

---

## 1. Objetivo

O componente `Panel` facilita a criação de áreas visuais separadas, com título e rodapé opcionais, sendo útil para destacar conteúdos em páginas Web ou sistemas visuais.  
Ele é construído como um componente filho de `Element` e pode ser facilmente customizado ou adaptado, isolando a lógica visual da lógica de negócio.

---

## 2. Implementação

### Arquivo: `Lib/Escala/Widgets/Container/panel.py`

```python
from Lib.Escala.Widgets.Base.element import Element

class Panel(Element):
    """
    Empacota elementos em painel Bootstrap
    Inspirado em Pablo Dall'Oglio.
    """

    def __init__(self, panel_title=None):
        super().__init__('div')
        self.class_ = 'panel panel-default'  # "class" é palavra reservada, usar "class_" para Python

        # Título do painel (opcional)
        if panel_title:
            head = Element('div')
            head.class_ = 'panel-heading'

            label = Element('h4')
            label.add(panel_title)

            title = Element('div')
            title.class_ = 'panel-title'
            title.add(label)
            head.add(title)
            super().add(head)

        # Corpo do painel
        self.body = Element('div')
        self.body.class_ = 'panel-body'
        super().add(self.body)

        # Rodapé do painel (opcional)
        self.footer = Element('div')
        self.footer.class_ = 'panel-footer'

    def add(self, content):
        """
        Adiciona conteúdo ao corpo do painel
        """
        self.body.add(content)

    def add_footer(self, footer):
        """
        Adiciona conteúdo ao rodapé do painel
        """
        self.footer.add(footer)
        super().add(self.footer)

    # Corrige o atributo 'class' para HTML
    def open(self):
        props = ''
        for name, value in self._properties.items():
            # Corrige class_ para class
            html_name = 'class' if name == 'class_' else name
            if isinstance(value, (str, int, float, bool)):
                props += f' {html_name}="{value}"'
        print(f"<{self.tagname}{props}>", end='')
```

---

## 3. Exemplo de Uso

### Arquivo: `app/Control/ExemploPanelControl.py`

```python
from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Container.panel import Panel

class ExemploPanelControl(Page):
    def __init__(self):
        super().__init__()
        
        panel = Panel('Título do painel')
        panel.style = 'margin: 20px'
        panel.add(' conteúdo conteúdo conteúdo conteúdo ')
        panel.add_footer('rodapé')
        
        self.add(panel)
```

---

## 4. Exibição

Para exibir o painel, instancie o controle e chame seu método `show()`:

```python
ctrl = ExemploPanelControl()
print(ctrl.show())
```

A saída será um HTML com a estrutura de painel, título, corpo e rodapé, no padrão Bootstrap.

---

## 5. Vantagens

- **Organização visual:** Separa conteúdos em áreas destacadas.
- **Customizável:** Mudanças de visual feitas apenas no componente.
- **Reaproveitamento:** Útil em várias partes do sistema.
- **Padronização:** Usa classes do Bootstrap, facilitando a integração com temas visuais modernos.

---

**Resumo:**  
O componente `Panel` é recomendado para criação de áreas visuais delimitadas, sendo flexível, reutilizável e alinhado ao desenvolvimento orientado a componentes proposto por Pablo Dall'Oglio.