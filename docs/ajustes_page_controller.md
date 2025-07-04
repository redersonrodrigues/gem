# Exemplo de Implementação do Padrão Page Controller em Python

Este documento explica, com base na arquitetura proposta por Pablo Dall'Oglio, como aplicar o padrão **Page Controller** em nossa aplicação Python. O exemplo é inspirado na estrutura apresentada nos livros de Pablo para PHP, mas adaptado ao contexto Python.

---

## 1. O que é o Page Controller?

O **Page Controller** é um padrão de projeto que centraliza o controle das ações de uma área específica de sua aplicação. Cada controller é responsável por processar requisições relativas a uma entidade ou funcionalidade, organizando a lógica de acordo com métodos que representam as ações possíveis (listar, criar, editar, etc).

---

## 2. Estrutura dos Arquivos

```
app/
  Control/
    PessoaControl.py
  Model/
    Pessoa.py
Lib/
  Escala/
    Core/
      app_loader.py
pessoas.py
```

---

## 3. Exemplo Prático

### 3.1. Modelo de Dados: Pessoa

Arquivo: `app/Model/Pessoa.py`

```python
class Pessoa:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

    @staticmethod
    def all():
        # Simula dados de banco de dados
        return [
            Pessoa(1, "Maria"),
            Pessoa(2, "José"),
            Pessoa(3, "Ana")
        ]
```

---

### 3.2. Page Controller: PessoaControl

Arquivo: `app/Control/PessoaControl.py`

```python
from app.Model.Pessoa import Pessoa

class PessoaControl:
    def listar(self):
        try:
            pessoas = Pessoa.all()
            for pessoa in pessoas:
                print(f"{pessoa.id} - {pessoa.nome}<br>")
        except Exception as e:
            print(e)

    def show(self, param):
        if param.get('method') == 'listar':
            self.listar()
```

- O método `listar()` executa a lógica de listagem.
- O método `show(param)` interpreta o parâmetro recebido e delega para o método correto.

---

### 3.3. Loader de Aplicação (AppLoader)

Arquivo: `Lib/Escala/Core/app_loader.py`

```python
import importlib

class AppLoader:
    @staticmethod
    def load_app_class(module_path, class_name):
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
```

---

### 3.4. Ponto de Entrada (Simulação do `pessoas.php`)

Arquivo: `pessoas.py`

```python
from Lib.Escala.Core.app_loader import AppLoader

# Carrega dinamicamente o controller
PessoaControlClass = AppLoader.load_app_class('app.Control.PessoaControl', 'PessoaControl')
controller = PessoaControlClass()

# Simula parâmetros de requisição (ex: vindos de URL ou formulário)
params = {'method': 'listar'}

controller.show(params)
```

---

## 4. Resultado Esperado

Ao executar `pessoas.py`, a saída será:

```
1 - Maria<br>
2 - José<br>
3 - Ana<br>
```

---

## 5. Benefícios do Padrão

- Centraliza a lógica de uma funcionalidade em uma única classe controller.
- Facilita a manutenção e a leitura do código.
- Permite a reutilização de loaders e controllers em pontos de entrada distintos.
- Segue o padrão MVC e as melhores práticas recomendadas por Pablo Dall'Oglio.

---

**Resumo:**  
Este exemplo demonstra como implementar o padrão Page Controller em Python, de forma fiel ao que Pablo Dall'Oglio ensina para PHP, promovendo organização, flexibilidade e escalabilidade em sua aplicação.
