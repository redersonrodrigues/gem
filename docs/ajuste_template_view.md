# Implementando Template View com Componentes (Padrão Pablo Dall'Oglio) em Python

Este documento mostra como aplicar o padrão **Template View** inspirado por Pablo Dall'Oglio, isolando a lógica Python da apresentação HTML. Aqui, substituímos a engine Twig por um carregador/renderer simples, mantendo a separação e a flexibilidade do padrão.

---

## 1. Estrutura Recomendada

```
app/
  Resources/
    form.html
app/
  Control/
    TemplateSampleControl.py
Lib/
  Escala/
    Core/
      template_loader.py
```

---

## 2. Arquivo de Template (HTML)

Arquivo: `app/Resources/form.html`

```html
<div class="panel panel-default" style="margin: 40px;">
  <div class="panel-heading">{{title}}</div>
  <div class="panel-body">
    <form action="{{action}}" method="POST" class="form-horizontal">
      <div class="form-group">
        <label class="col-sm-2 control-label"> Nome </label>
        <div class="col-sm-10">
            <input type="text" name="nome" value="{{nome}}" class="form-control">
        </div>
      </div>
      
      <div class="form-group">
        <label class="col-sm-2 control-label"> Endereço </label>
        <div class="col-sm-10">
            <input type="text" name="endereco" value="{{endereco}}" class="form-control">
        </div>
      </div>
      
      <div class="form-group">
        <label class="col-sm-2 control-label"> Telefone </label>
        <div class="col-sm-10">
            <input type="text" name="telefone" value="{{telefone}}" class="form-control">
        </div>
      </div>
      
      <div class="form-group">
      <div class="col-sm-offset-2 col-sm-8">
      <input type="submit" class="btn btn-success" value="enviar">
      </div>
      </div>
    </form>
    </div>
  </div>
</div>
```

---

## 3. Loader do Template

Arquivo: `Lib/Escala/Core/template_loader.py`

```python
import os

class TemplateLoader:
    """
    Carrega e substitui variáveis simples em templates HTML no estilo {{ variavel }}
    """
    def __init__(self, base_path='app/Resources'):
        self.base_path = base_path

    def render(self, filename, context):
        path = os.path.join(self.base_path, filename)
        with open(path, encoding='utf-8') as f:
            html = f.read()
        for key, value in context.items():
            html = html.replace('{{' + key + '}}', str(value))
        return html
```

---

## 4. Controller de Exemplo

Arquivo: `app/Control/TemplateSampleControl.py`

```python
from Lib.Escala.Control.Page import Page
from Lib.Escala.Core.template_loader import TemplateLoader

class TemplateSampleControl(Page):
    def __init__(self):
        super().__init__()
        self.template_loader = TemplateLoader('app/Resources')

    def show(self, param=None):
        # Dados fixos (em produção, viriam do banco de dados)
        replaces = {
            'title': 'Título',
            'action': '?class=TemplateSampleControl&method=onGravar',
            'nome': 'Maria',
            'endereco': 'Rua das flores',
            'telefone': '(51) 1234-5678'
        }
        return self.template_loader.render('form.html', replaces)

    def onGravar(self, param):
        # Exibe os dados submetidos (simulação de POST)
        return f"<pre>{param}</pre>"
```

---

## 5. Como Usar/Testar

1. **Inclua o Controller no Front Controller**  
   Altere o método que exibe páginas para chamar `TemplateSampleControl`:

   ```python
   self.show_page('TemplateSampleControl')
   ```

2. **Abra a aplicação.**  
   O formulário deve aparecer com os dados definidos no contexto.

3. **Submeta os dados.**  
   O método `onGravar` será chamado (simule a coleta dos dados no ambiente desktop/web).

---

## 6. Vantagens

- **Isolamento total** da lógica Python da apresentação HTML.
- **Reaproveitamento:** O mesmo template pode ser renderizado com diferentes dados/contextos.
- **Fácil manutenção:** Mudanças visuais são feitas só no arquivo HTML.
- **Flexível:** Permite evoluir para engines de template mais sofisticadas (Jinja2, etc) sem mudar a lógica do controller.

---

**Resumo:**  
Usando o padrão Template View, você separa a lógica da apresentação seguindo a linhagem de componentes de Pablo Dall'Oglio, tornando o sistema mais limpo, flexível e sustentável.
