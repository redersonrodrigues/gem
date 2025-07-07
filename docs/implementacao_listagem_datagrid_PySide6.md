# Implementação de Listagem com Datagrid (Padrão PySide6)

Este documento explica como implementar listagens (grids) reutilizáveis e padronizadas na aplicação, seguindo o padrão de Pablo Dall'Oglio, utilizando as classes Datagrid, DatagridColumn e DatagridWrapper adaptadas para Python e PySide6.

---

## 1. Estrutura dos Componentes

- **Datagrid:** Gerencia colunas, itens e ações da listagem.
- **DatagridColumn:** Define as propriedades de cada coluna (nome, rótulo, alinhamento, largura, ação, transformação).
- **DatagridWrapper:** Decora e exibe a grid em formato visual responsivo, integrando com Panel e Element.

---

## 2. Passos para Implementação

### 2.1. Defina o Modelo

Exemplo:

```python
class Especializacao:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome
```

### 2.2. Crie a Datagrid e Colunas

```python
from Lib.Escala.Widgets.Datagrid.Datagrid import Datagrid
from Lib.Escala.Widgets.Datagrid.DatagridColumn import DatagridColumn
from Lib.Escala.Widgets.Wrapper.DatagridWrapper import DatagridWrapper

grid = Datagrid()
grid.addColumn(DatagridColumn('id', 'ID', 'center', '60px'))
grid.addColumn(DatagridColumn('nome', 'Nome', 'left', '200px'))
```

### 2.3. Adicione Ações (Opcional)

```python
def editar_callback(key):
    print(f'Editar {key}')

grid.addAction('Editar', editar_callback, 'id', image='ico_edit.png')
```

### 2.4. Adicione os Itens

```python
especializacoes = [
    Especializacao(1, 'Cardiologia'),
    Especializacao(2, 'Neurologia'),
]
for esp in especializacoes:
    grid.addItem(esp)
```

### 2.5. Exiba a Grid

```python
wrapper = DatagridWrapper(grid)
wrapper.show()
```

---

## 3. Exemplo Real Completo

```python
from Lib.Escala.Widgets.Datagrid.Datagrid import Datagrid
from Lib.Escala.Widgets.Datagrid.DatagridColumn import DatagridColumn
from Lib.Escala.Widgets.Wrapper.DatagridWrapper import DatagridWrapper
from app.Model.especializacao import Especializacao

def editar_callback(key):
    print(f'Editar {key}')

grid = Datagrid()
grid.addColumn(DatagridColumn('id', 'ID', 'center', '60px'))
grid.addColumn(DatagridColumn('nome', 'Nome', 'left', '200px'))
grid.addAction('Editar', editar_callback, 'id', image='ico_edit.png')

# Carregando dados do banco ou mock
especializacoes = [
    Especializacao(1, 'Cardiologia'),
    Especializacao(2, 'Neurologia'),
]
for esp in especializacoes:
    grid.addItem(esp)

wrapper = DatagridWrapper(grid)
wrapper.show()
```

---

## 4. Dicas e Boas Práticas

- Use o método `setTransformer` em DatagridColumn para customizar a exibição de valores (ex: datas, status, etc).
- Para ações, utilize funções/callbacks que recebam o valor da chave do item.
- O visual pode ser customizado via CSS ou ajustando as classes do Panel/Element.
- Consulte exemplos reais em `app/Control/` para integração com controllers e navegação.

---

## 5. Exemplos Avançados de Listagem (Inspirados em Pablo Dall'Oglio)

### 5.1. Listagem com Dados Estáticos

```python
from Lib.Escala.Widgets.Datagrid.Datagrid import Datagrid
from Lib.Escala.Widgets.Datagrid.DatagridColumn import DatagridColumn
from Lib.Escala.Widgets.Wrapper.DatagridWrapper import DatagridWrapper

class Pessoa:
    def __init__(self, id, nome, email):
        self.id = id
        self.nome = nome
        self.email = email

# Dados estáticos
pessoas = [
    Pessoa(1, 'João', 'joao@email.com'),
    Pessoa(2, 'Maria', 'maria@email.com'),
]

grid = Datagrid()
grid.addColumn(DatagridColumn('id', 'ID', 'center', '60px'))
grid.addColumn(DatagridColumn('nome', 'Nome', 'left', '150px'))
grid.addColumn(DatagridColumn('email', 'E-mail', 'left', '200px'))
for p in pessoas:
    grid.addItem(p)
DatagridWrapper(grid).show()
```

---

### 5.2. Listagem com Ações e Transformações

```python
def editar_callback(key):
    print(f'Editar registro {key}')
def email_transformer(email):
    return email.lower()

grid = Datagrid()
grid.addColumn(DatagridColumn('id', 'ID', 'center', '60px'))
col_nome = DatagridColumn('nome', 'Nome', 'left', '150px')
grid.addColumn(col_nome)
col_email = DatagridColumn('email', 'E-mail', 'left', '200px')
col_email.setTransformer(email_transformer)
grid.addColumn(col_email)
grid.addAction('Editar', editar_callback, 'id', image='ico_edit.png')
for p in pessoas:
    grid.addItem(p)
DatagridWrapper(grid).show()
```

---

### 5.3. Listagem com Dados do Banco de Dados

```python
from app.Model.Pessoa import Pessoa
# Supondo que Pessoa.all() retorna lista de objetos Pessoa
pessoas = Pessoa.all()

grid = Datagrid()
grid.addColumn(DatagridColumn('id', 'ID', 'center', '60px'))
grid.addColumn(DatagridColumn('nome', 'Nome', 'left', '150px'))
grid.addColumn(DatagridColumn('email', 'E-mail', 'left', '200px'))
for p in pessoas:
    grid.addItem(p)
DatagridWrapper(grid).show()
```

---

### 5.4. Listagem com Formulário de Busca

```python
from Lib.Escala.Widgets.Form.Form import Form
from Lib.Escala.Widgets.Form.Entry import Entry
from Lib.Escala.Widgets.Form.Button import Button
from Lib.Escala.Widgets.Wrapper.FormWrapper import FormWrapper

# Formulário de busca
form = Form('busca_pessoa')
form.addField('Nome', Entry('nome'))
form.addAction('Buscar', lambda x: print('Buscar:', x))
FormWrapper(form).show()

# Após submissão, filtre os dados:
# nome_filtro = ... (obtido do form)
pessoas_filtradas = [p for p in pessoas if nome_filtro.lower() in p.nome.lower()]
# Exiba a grid normalmente
```

---

## 6. Observações

- Use transformações para customizar a exibição de dados (ex: formatar datas, status, etc).
- Ações podem ser links, botões ou ícones, e recebem o valor do campo chave.
- Para integração com banco, utilize métodos do seu Model (ex: `Pessoa.all()`, `Pessoa.filter(...)`).
- O formulário de busca pode ser integrado ao controller para filtrar e atualizar a grid dinamicamente.

---

**Resumo:**
A implementação de listagens com Datagrid permite criar telas de consulta e manutenção de dados de forma padronizada, reutilizável e fácil de manter, seguindo o padrão de componentes do livro de Pablo Dall'Oglio, adaptado para PySide6.
