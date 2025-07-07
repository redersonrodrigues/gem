# Documentação Técnica dos Componentes de Formulário e Wrapper

Este documento detalha tecnicamente todos os componentes presentes em `Lib/Escala/Widgets/Form` e `Lib/Escala/Widgets/Wrapper`, com foco em uso real, integração e replicação por outros desenvolvedores.

---

## 1. Formulários: Estrutura e Componentes

### 1.1. Form (Formulário)

Classe principal para construção de formulários dinâmicos.

- **Arquivo:** `Form.py`
- **Principais métodos:**
  - `addField(label, obj, size='100%')`: adiciona um campo (objeto Field) ao formulário.
  - `addAction(label, action)`: adiciona uma ação (botão) ao formulário.
  - `setData(obj)`: preenche os campos a partir de um objeto/dict.
  - `getData(cls=dict, post_data=None, files_data=None)`: extrai os dados do formulário para um objeto ou dict.
  - `setTitle(title)`: define o título do formulário.
  - `getFields()`, `getActions()`, `getName()`, `getTitle()`

**Exemplo real:**

```python
form = Form('usuario_form')
form.setTitle('Cadastro de Usuário')
form.addField('Nome', Entry('nome'))
form.addField('Senha', Password('senha'))
form.addAction('Salvar', on_save)
```

### 1.2. Field e Subclasses

Base para todos os campos de formulário. Cada campo herda de `Field` e implementa seu próprio método de renderização.

- **Arquivo:** `Field.py` e subclasses
- **Principais campos:**
  - `Entry` (caixa de texto)
  - `Password` (senha)
  - `Combo` (select)
  - `RadioGroup`/`RadioButton` (opções)
  - `CheckGroup`/`CheckButton` (checkboxes)
  - `Date` (data)
  - `File` (upload)
  - `Hidden` (campo oculto)
  - `Label` (texto)

**Exemplo real:**

```python
nome = Entry('nome')
nome.setValue('Maria')
senha = Password('senha')
combo = Combo('perfil', items=['Admin', 'Usuário'])
```

### 1.3. Button

Botão de ação do formulário.

- **Arquivo:** `Button.py`
- **Principais métodos:**
  - `setFormName(name)`: associa ao formulário.
  - `setAction(action, label)`: define ação e rótulo.

**Exemplo:**

```python
btn = Button('salvar')
btn.setFormName('usuario_form')
btn.setAction(on_save, 'Salvar')
```

### 1.4. SimpleForm

Componente simplificado para prototipação rápida.

- **Arquivo:** `SimpleForm.py`
- **Uso:**

```python
form = SimpleForm('meu_form')
form.set_title('Cadastro')
form.add_field('Nome', 'nome', 'text', '', 'form-control')
form.set_action('?class=SimpleFormControl&method=onGravar')
```

### 1.5. FormElementInterface

Interface para padronizar elementos de formulário customizados.

### 1.6. Componentes de Campo Específicos

#### CheckButton e CheckGroup

- **CheckButton:** Campo de checkbox individual.
- **CheckGroup:** Agrupa múltiplos CheckButton para seleção múltipla.
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.CheckButton import CheckButton
from Lib.Escala.Widgets.Form.CheckGroup import CheckGroup

cb1 = CheckButton('receber_email')
cb1.setLabel('Receber e-mail')
cb2 = CheckButton('aceitar_termos')
cb2.setLabel('Aceitar termos')
check_group = CheckGroup('preferencias')
check_group.add(cb1)
check_group.add(cb2)
```

#### Combo

- **Combo:** Campo de seleção (dropdown/select).
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Combo import Combo
combo = Combo('perfil')
combo.addItems(['Admin', 'Usuário', 'Visitante'])
combo.setValue('Usuário')
```

#### Date

- **Date:** Campo para seleção de data.
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Date import Date
date = Date('data_nascimento')
date.setValue('1990-01-01')
```

#### Entry

- **Entry:** Campo de texto simples (input type="text").
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Entry import Entry
entry = Entry('nome')
entry.setValue('Maria')
```

#### File

- **File:** Campo para upload de arquivos.
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.File import File
file = File('curriculo')
```

#### Hidden

- **Hidden:** Campo oculto (input type="hidden").
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Hidden import Hidden
hidden = Hidden('id_usuario')
hidden.setValue('123')
```

#### Label

- **Label:** Exibe texto estático no formulário.
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Label import Label
label = Label('Observação: preencha todos os campos.')
```

#### Password

- **Password:** Campo de senha (input type="password").
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Password import Password
senha = Password('senha')
```

#### RadioButton e RadioGroup

- **RadioButton:** Opção individual de seleção única.
- **RadioGroup:** Agrupa RadioButtons para escolha única.
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.RadioButton import RadioButton
from Lib.Escala.Widgets.Form.RadioGroup import RadioGroup

rb1 = RadioButton('sexo', 'M', 'Masculino')
rb2 = RadioButton('sexo', 'F', 'Feminino')
group = RadioGroup('sexo')
group.add(rb1)
group.add(rb2)
```

#### Text

- **Text:** Campo de texto multilinha (textarea).
- **Exemplo:**

```python
from Lib.Escala.Widgets.Form.Text import Text
obs = Text('observacoes')
obs.setValue('Digite aqui suas observações...')
```

---

## 2. Wrapper: Layout e Decoração

### 2.1. FormWrapper

Decorator para apresentação visual padronizada (Bootstrap-like).

- **Arquivo:** `FormWrapper.py`
- **Como funciona:**
  - Recebe um objeto `Form` e gera a estrutura visual (campos, labels, botões) com classes e layout responsivo.
  - Utiliza `Panel` para agrupar e destacar o formulário.
  - Adiciona rodapé com botões de ação.

**Exemplo real:**

```python
form = Form('usuario_form')
form.addField('Nome', Entry('nome'))
form.addAction('Salvar', on_save)
wrapper = FormWrapper(form)
print(wrapper.render())
```

**Fluxo interno:**

- Cria um `<form class='form-horizontal'>`.
- Para cada campo, gera um `<div class='form-group'>` com `<label>` e campo.
- Adiciona botões no rodapé (`btn btn-success`, `btn btn-default`).
- Envolve tudo em um `Panel` com título.

---

## 3. Recomendações e Boas Práticas

- Sempre use os componentes prontos para garantir padronização visual e de comportamento.
- Para campos customizados, herde de `Field` e implemente `render()`.
- Use `FormWrapper` para garantir responsividade e visual consistente.
- Consulte exemplos reais em `app/Control/SimpleFormControl.py` e `app/Control/ExemploPanelControl.py`.

---

## 4. Exemplo Completo de Integração

```python
from Lib.Escala.Widgets.Form.Form import Form
from Lib.Escala.Widgets.Form.Entry import Entry
from Lib.Escala.Widgets.Form.Button import Button
from Lib.Escala.Widgets.Wrapper.FormWrapper import FormWrapper

form = Form('cadastro')
form.setTitle('Cadastro de Usuário')
form.addField('Nome', Entry('nome'))
form.addField('Senha', Entry('senha'))
form.addAction('Salvar', lambda x: print('Salvo!'))

wrapper = FormWrapper(form)
print(wrapper.render())
```

---

## 5. Dicas Avançadas e Integração

### 5.1. Integração de Campos Diversos em um Único Formulário

Você pode combinar todos os campos apresentados em um mesmo formulário, aproveitando a flexibilidade dos componentes:

```python
from Lib.Escala.Widgets.Form.Form import Form
from Lib.Escala.Widgets.Form.Entry import Entry
from Lib.Escala.Widgets.Form.Password import Password
from Lib.Escala.Widgets.Form.Combo import Combo
from Lib.Escala.Widgets.Form.Date import Date
from Lib.Escala.Widgets.Form.CheckButton import CheckButton
from Lib.Escala.Widgets.Form.CheckGroup import CheckGroup
from Lib.Escala.Widgets.Form.RadioButton import RadioButton
from Lib.Escala.Widgets.Form.RadioGroup import RadioGroup
from Lib.Escala.Widgets.Form.File import File
from Lib.Escala.Widgets.Form.Hidden import Hidden
from Lib.Escala.Widgets.Form.Label import Label
from Lib.Escala.Widgets.Form.Text import Text
from Lib.Escala.Widgets.Wrapper.FormWrapper import FormWrapper

form = Form('cadastro_completo')
form.setTitle('Cadastro Completo')
form.addField('Nome', Entry('nome'))
form.addField('Senha', Password('senha'))
form.addField('Perfil', Combo('perfil', items=['Admin', 'Usuário']))
form.addField('Nascimento', Date('data_nascimento'))

cb1 = CheckButton('newsletter')
cb1.setLabel('Receber novidades')
cb2 = CheckButton('termos')
cb2.setLabel('Aceitar termos')
check_group = CheckGroup('preferencias')
check_group.add(cb1)
check_group.add(cb2)
form.addField('Preferências', check_group)

rb1 = RadioButton('sexo', 'M', 'Masculino')
rb2 = RadioButton('sexo', 'F', 'Feminino')
group = RadioGroup('sexo')
group.add(rb1)
group.add(rb2)
form.addField('Sexo', group)

form.addField('Currículo', File('curriculo'))
form.addField('', Hidden('id_usuario'))
form.addField('Observação', Label('Preencha todos os campos obrigatórios.'))
form.addField('Sobre você', Text('sobre'))
form.addAction('Salvar', lambda x: print('Salvo!'))

wrapper = FormWrapper(form)
print(wrapper.render())
```

### 5.2. Customização de Campos

Todos os campos permitem customização de atributos, como classes CSS, valores iniciais, tamanhos, etc. Exemplo:

```python
entry = Entry('nome')
entry.class_ = 'form-control form-control-lg'
entry.setValue('João')
```

### 5.3. Validação e Processamento

Implemente validação no controller antes de processar os dados recebidos do formulário. Use `getData()` para extrair os valores preenchidos.

### 5.4. Criação de Novos Campos

Para criar um novo tipo de campo, herde de `Field` e implemente o método `render()` conforme a necessidade.

---

## 6. Referências e Exemplos no Projeto

- Veja exemplos reais em `app/Control/SimpleFormControl.py`, `app/Control/ExemploPanelControl.py` e nos arquivos de teste em `app/Control/`.
- Consulte também os arquivos de documentação em `docs/` para padrões de arquitetura e integração.

---

**Dúvidas ou sugestões? Consulte a equipe de desenvolvimento ou contribua com exemplos e melhorias neste documento.**
