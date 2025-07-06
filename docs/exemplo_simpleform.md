# Exemplo de Uso do Componente SimpleForm

Este documento explica como implementar e utilizar o componente **SimpleForm** inspirado no conceito apresentado por Pablo Dall'Oglio, adaptado para Python. O objetivo é demonstrar como criar, configurar e exibir rapidamente um formulário HTML simples e reutilizável, facilitando o desenvolvimento e a manutenção da interface da aplicação.

---

## 1. O que é o SimpleForm?

O `SimpleForm` é um componente de formulário genérico que permite definir:
- Um nome para o formulário;
- Um título;
- Campos de diferentes tipos;
- Uma ação (URL) de submissão.

Ele isola o código de montagem do HTML, facilitando a reutilização e a alteração do visual ou da lógica de todos os formulários do sistema em um único lugar.

---

## 2. Estrutura do Componente

Arquivo: `Lib/Escala/Widgets/Form/simple_form.py`

```python
class SimpleForm:
    def __init__(self, name):
        self.name = name
        self.fields = []
        self.title = ''
        self.action = ''

    def set_title(self, title):
        self.title = title

    def add_field(self, label, name, field_type, value, css_class=''):
        self.fields.append({
            'label': label,
            'name': name,
            'type': field_type,
            'value': value,
            'class': css_class,
        })

    def set_action(self, action):
        self.action = action

    def render(self):
        html = []
        html.append("<div class='panel panel-default' style='margin: 40px;'>")
        html.append(f"<div class='panel-heading'> {self.title} </div>")
        html.append("<div class='panel-body'>")
        html.append(f"<form method='POST' action='{self.action}' class='form-horizontal'>")
        if self.fields:
            for field in self.fields:
                html.append("<div class='form-group'>")
                html.append(f"<label class='col-sm-2 control-label'> {field['label']} </label>")
                html.append("<div class='col-sm-10'>")
                html.append(
                    f"<input type='{field['type']}' name='{field['name']}' "
                    f"value='{field['value']}' class='{field['class']}'>"
                )
                html.append("</div>")
                html.append("</div>")
            html.append("<div class='form-group'>")
            html.append("<div class='col-sm-offset-2 col-sm-8'>")
            html.append("<input type='submit' class='btn btn-success' value='enviar'>")
            html.append("</div>")
            html.append("</div>")
        html.append("</form>")
        html.append("</div>")
        html.append("</div>")
        return "\n".join(html)
```

---

## 3. Exemplo de Utilização em um Controller

Arquivo: `app/Control/SimpleFormControl.py`

```python
from Lib.Escala.Control.Page import Page
from Lib.Escala.Widgets.Form.simple_form import SimpleForm

class SimpleFormControl(Page):
    def __init__(self):
        super().__init__()
        self.form = SimpleForm('my_form')
        self.form.set_title('Título')
        self.form.add_field('Nome', 'nome', 'text', 'Maria', 'form-control')
        self.form.add_field('Endereço', 'endereco', 'text', 'Rua das flores', 'form-control')
        self.form.add_field('Telefone', 'telefone', 'text', '(51) 1234-5678', 'form-control')
        # Define ação apontando para o Front Controller, passando parâmetros da classe e método
        self.form.set_action('?class=SimpleFormControl&method=onGravar')

    def show(self, param=None):
        # Exibe o formulário (chamado pelo Front Controller)
        return self.form.render()

    def onGravar(self, param):
        # Exibe os dados recebidos via POST (simulação)
        return f"<pre>{param}</pre>"
```

---

## 4. Como Testar

1. **Adicione o SimpleFormControl ao Front Controller**  
   No ponto de entrada da aplicação (`main.py`), faça a chamada para a página de teste do formulário:
   ```python
   self.show_page('SimpleFormControl')
   ```

2. **Execute o sistema**  
   Rode o aplicativo e acesse a interface. O formulário será exibido com os campos definidos.

3. **Preencha e envie**  
   Ao clicar em "enviar", o método `onGravar` será chamado e mostrará os dados enviados (em uma implementação real, você processaria os dados conforme a necessidade).

---

## 5. Vantagens do SimpleForm

- **Reaproveitamento:** O mesmo componente pode ser usado para diversos formulários, bastando configurar campos e ações.
- **Padronização:** Garante consistência visual e estrutural nos formulários do sistema.
- **Facilidade de manutenção:** Qualquer ajuste na lógica ou no visual do formulário pode ser feito em um só lugar.
- **Separação de responsabilidades:** O controller apenas define o que aparecerá no formulário, sem se preocupar com HTML.

---

## 6. Recomendações

- Este exemplo é ideal para prototipação rápida ou telas simples.
- Para formulários mais complexos ou dinâmicos, é recomendável evoluir para componentes mais sofisticados, mas mantendo o padrão de isolamento e reutilização.
- Adapte o método `onGravar` para processar realmente os dados recebidos, conforme a lógica da sua aplicação.

---

**Resumo:**  
O SimpleForm é um exemplo de como aplicar os conceitos de Pablo Dall'Oglio para isolar, padronizar e facilitar o uso de formulários em sistemas Python, tornando o código mais limpo, reutilizável e fácil de manter.