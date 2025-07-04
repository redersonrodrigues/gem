# Como aplicar o padrão Strategy para Escalas mantendo a estrutura do livro de Pablo Dall'Oglio

Este documento detalha, passo a passo, como inserir o padrão de projeto **Strategy** para lidar com diferentes lógicas de escalas (plantonista e sobreaviso) em um sistema baseado na arquitetura do capítulo 8 do livro de Pablo Dall'Oglio, **sem alterar a estrutura de Repository, Criteria e Record** já existente.

---

## **1. Conceito**

- **Repository, Criteria e Record** continuam sendo responsáveis pela persistência, filtragem e representação de entidades.
- **Strategy** será usada para encapsular regras de negócio que variam conforme o tipo de escala (plantonista/sobreaviso), sem misturar lógica de domínio com persistência.
- O **context** (serviço ou fachada) irá delegar para a strategy apropriada, tornando o sistema aberto para extensão e fechado para modificação (princípio OCP/SOLID).

---

## **2. Estrutura dos diretórios sugerida**

```
app/
  Model/
    escala_plantonista.py
    escala_sobreaviso.py
  Strategy/
    escala_strategy.py
    escala_factory.py
  Service/
    gerenciador_escalas.py
Lib/
  Escala/
    Database/
      record.py
      repository.py
      criteria.py
docs/
  ajuste_escalas_strategy_testes.md
tests/
  test_escala_plantonista.py
  test_escala_sobreaviso.py
```

---

## **3. Implementação passo a passo**

### **Passo 1: Mantenha os Models e infraestrutura do livro**

Exemplo de Model (ActiveRecord):

```python
# app/Model/escala_plantonista.py
from Lib.Escala.Database.record import Record

class EscalaPlantonista(Record):
    TABLENAME = "escala_plantonista"
    def __init__(self, id=None, data=None, turno=None, medico_0_id=None, medico_1_id=None):
        super().__init__(
            id=id, data=data, turno=turno,
            medico_0_id=medico_0_id, medico_1_id=medico_1_id
        )
```

---

### **Passo 2: Crie a interface da Strategy**

```python
# app/Strategy/escala_strategy.py
from abc import ABC, abstractmethod

class EscalaStrategy(ABC):
    @abstractmethod
    def criar_escala(self, **kwargs):
        pass

    @abstractmethod
    def buscar_escala(self, **kwargs):
        pass
```

---

### **Passo 3: Implemente as estratégias concretas**

```python
# app/Strategy/escala_strategy.py (continuação)
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_plantonista import EscalaPlantonista
from app.Model.escala_sobreaviso import EscalaSobreaviso

class EscalaPlantonistaStrategy(EscalaStrategy):
    def criar_escala(self, **kwargs):
        escala = EscalaPlantonista(
            data=kwargs["data"], turno=kwargs["turno"],
            medico_0_id=kwargs["medico_0_id"], medico_1_id=kwargs["medico_1_id"]
        )
        escala.store()
        return escala

    def buscar_escala(self, **kwargs):
        c = Criteria()
        if "data" in kwargs:
            c.add("data", "=", kwargs["data"])
        if "turno" in kwargs:
            c.add("turno", "=", kwargs["turno"])
        repo = Repository(EscalaPlantonista)
        return repo.load(c)

class EscalaSobreavisoStrategy(EscalaStrategy):
    def criar_escala(self, **kwargs):
        escala = EscalaSobreaviso(
            data_inicial=kwargs["data_inicial"],
            data_final=kwargs["data_final"],
            medico_id=kwargs["medico_id"],
            especializacao_id=kwargs["especializacao_id"]
        )
        escala.store()
        return escala

    def buscar_escala(self, **kwargs):
        c = Criteria()
        if "data" in kwargs:
            c.add("data_inicial", "<=", kwargs["data"])
            c.add("data_final", ">=", kwargs["data"])
        repo = Repository(EscalaSobreaviso)
        return repo.load(c)
```

---

### **Passo 4: Crie a Factory de estratégias**

```python
# app/Strategy/escala_factory.py
from app.Strategy.escala_strategy import EscalaPlantonistaStrategy, EscalaSobreavisoStrategy

class EscalaFactory:
    @staticmethod
    def get_strategy(tipo_escala):
        if tipo_escala == "plantonista":
            return EscalaPlantonistaStrategy()
        elif tipo_escala == "sobreaviso":
            return EscalaSobreavisoStrategy()
        else:
            raise ValueError("Tipo de escala desconhecido")
```

---

### **Passo 5: Implemente o Context (serviço/fachada)**

```python
# app/Service/gerenciador_escalas.py
from app.Strategy.escala_factory import EscalaFactory

class GerenciadorEscalas:
    def __init__(self, tipo_escala):
        self._strategy = EscalaFactory.get_strategy(tipo_escala)

    def set_tipo_escala(self, tipo_escala):
        self._strategy = EscalaFactory.get_strategy(tipo_escala)

    def criar_escala(self, **kwargs):
        return self._strategy.criar_escala(**kwargs)

    def buscar_escala(self, **kwargs):
        return self._strategy.buscar_escala(**kwargs)
```

---

### **Passo 6: Testes automatizados**

```python
# tests/test_escala_plantonista.py
import pytest
from app.Service.gerenciador_escalas import GerenciadorEscalas
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_plantonista import EscalaPlantonista

@pytest.fixture(autouse=True)
def transacao():
    from Lib.Escala.Database.transaction import Transaction
    Transaction.open("escala")
    yield
    Transaction.close()

def test_criar_e_buscar_escala_plantonista():
    # Limpa escalas duplicadas antes do teste
    repo = Repository(EscalaPlantonista)
    c = Criteria()
    c.add("data", "=", "2025-07-10")
    c.add("turno", "=", "diurno")
    c.add("medico_0_id", "=", 1)
    c.add("medico_1_id", "=", 2)
    repo.delete(c)

    ger = GerenciadorEscalas("plantonista")
    escala = ger.criar_escala(data="2025-07-10", turno="diurno", medico_0_id=1, medico_1_id=2)
    assert escala.id is not None

    escalas = ger.buscar_escala(data="2025-07-10")
    assert any(e.id == escala.id for e in escalas)

# tests/test_escala_sobreaviso.py
import pytest
from app.Service.gerenciador_escalas import GerenciadorEscalas
from Lib.Escala.Database.repository import Repository
from Lib.Escala.Database.criteria import Criteria
from app.Model.escala_sobreaviso import EscalaSobreaviso

@pytest.fixture(autouse=True)
def transacao():
    from Lib.Escala.Database.transaction import Transaction
    Transaction.open("escala")
    yield
    Transaction.close()

def test_criar_e_buscar_escala_sobreaviso():
    # Limpa escalas duplicadas antes do teste
    repo = Repository(EscalaSobreaviso)
    c = Criteria()
    c.add("data_inicial", "=", "2025-07-10")
    c.add("data_final", "=", "2025-07-12")
    c.add("medico_id", "=", 1)
    c.add("especializacao_id", "=", 1)
    repo.delete(c)

    ger = GerenciadorEscalas("sobreaviso")
    escala = ger.criar_escala(data_inicial="2025-07-10", data_final="2025-07-12", medico_id=1, especializacao_id=1)
    assert escala.id is not None

    escalas = ger.buscar_escala(data="2025-07-11")
    assert any(e.id == escala.id for e in escalas)
```

---

## **4. Dicas e boas práticas**

- Cada strategy pode usar qualquer lógica de negócio, validação, etc, mas sempre usando Repository/Criteria conforme o livro.
- O contexto/fachada pode ser expandido para receber dependências adicionais (ex: logs, transação, etc).
- O padrão mantém o código limpo, testável e preparado para crescer.
- Teste cada strategy isoladamente!

---

## **5. Referências**

- Livro: "PHP Programando com Orientação a Objetos", Pablo Dall'Oglio, Capítulo 8.
- Padrão Strategy: https://refactoring.guru/pt-br/design-patterns/strategy
- Este documento foi gerado para orientar a evolução do sistema GEM mantendo compatibilidade e boas práticas.

---
