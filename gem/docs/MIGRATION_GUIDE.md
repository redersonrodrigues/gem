# Guia de Migração - Estrutura Antiga para Nova Estrutura MVC

## Mapeamento de Arquivos

### Antes (Estrutura Antiga)
```
app/
├── __init__.py
├── models.py        # Todos os modelos
├── crud.py          # Operações CRUD
├── database.py      # Configuração do banco
└── populate_specializations.py
```

### Depois (Nova Estrutura MVC)
```
gem/
├── models/
│   ├── __init__.py
│   ├── base_models.py      # Hospital, Medico, Especializacao, User, Log
│   └── escala_models.py    # Escalas com Strategy Pattern
├── repositories/
│   ├── __init__.py
│   ├── base_repository.py  # Repositório base
│   ├── hospital_repository.py
│   ├── medico_repository.py
│   └── especializacao_repository.py
├── services/
│   ├── __init__.py
│   ├── hospital_service.py
│   ├── medico_service.py
│   └── especializacao_service.py
├── controllers/
│   ├── __init__.py
│   ├── base_controller.py
│   ├── hospital_controller.py
│   └── medico_controller.py
├── utils/
│   ├── __init__.py
│   └── database.py         # Migrado de app/database.py
└── app.py                  # Configuração principal
```

## Mudanças nos Imports

### Antes
```python
from app.models import db, Hospital, Medico, Especializacao
from app.crud import create_hospital, get_hospitals, update_hospital
from app.database import init_db
```

### Depois
```python
# Modelos
from gem.models import Hospital, Medico, Especializacao
from gem.utils.database import db, init_db

# Usando repositórios
from gem.repositories import HospitalRepository
hospital_repo = HospitalRepository()
hospital = hospital_repo.create_hospital("Nome", "Endereço")

# Usando serviços (recomendado)
from gem.services import HospitalService
hospital_service = HospitalService()
resultado = hospital_service.criar_hospital("Nome", "Endereço")

# Usando controladores (para interfaces)
from gem.controllers import HospitalController
controller = HospitalController()
resposta = controller.criar_hospital("Nome", "Endereço")
```

## Equivalência de Funções

### CRUD Antigo → Novo Padrão

#### Hospital
```python
# ANTES
from app.crud import create_hospital, get_hospitals, update_hospital, delete_hospital

# DEPOIS - Repository
from gem.repositories import HospitalRepository
repo = HospitalRepository()
repo.create_hospital(nome, endereco)
repo.get_hospitals()
repo.update_hospital(id, nome, endereco)
repo.delete_hospital(id)

# DEPOIS - Service (Recomendado)
from gem.services import HospitalService
service = HospitalService()
service.criar_hospital(nome, endereco)
service.listar_hospitais()
service.atualizar_hospital(id, nome, endereco)
service.excluir_hospital(id)

# DEPOIS - Controller (Para UI)
from gem.controllers import HospitalController
controller = HospitalController()
controller.criar_hospital(nome, endereco)
controller.listar_hospitais()
controller.atualizar_hospital(id, nome, endereco)
controller.excluir_hospital(id)
```

#### Médico
```python
# ANTES
from app.crud import create_medico, get_medicos, update_medico, delete_medico

# DEPOIS - Service
from gem.services import MedicoService
service = MedicoService()
service.criar_medico(nome)
service.listar_medicos()
service.atualizar_medico(id, nome)
service.excluir_medico(id)
```

#### Especialização
```python
# ANTES
from app.crud import create_especializacao, get_especializacoes, update_especializacao, delete_especializacao

# DEPOIS - Service
from gem.services import EspecializacaoService
service = EspecializacaoService()
service.criar_especializacao(nome)
service.listar_especializacoes()
service.atualizar_especializacao(id, nome)
service.excluir_especializacao(id)
```

## Vantagens da Nova Estrutura

### 1. Separação de Responsabilidades
- **Models**: Apenas definição de entidades
- **Repositories**: Acesso a dados
- **Services**: Lógica de negócio e validações
- **Controllers**: Interface e coordenação

### 2. Validação Centralizada
```python
# Antes: Validação espalhada ou inexistente
hospital = Hospital(nome="", endereco="")  # Sem validação

# Depois: Validação nos serviços
try:
    hospital = hospital_service.criar_hospital("", "")
except ValueError as e:
    print(f"Erro: {e}")  # "Nome do hospital é obrigatório"
```

### 3. Respostas Padronizadas
```python
# Controllers retornam formato padronizado
resposta = controller.criar_hospital("Hospital X", "Rua Y")
# {
#   'success': True,
#   'data': {'id': 1, 'nome': 'Hospital X', 'endereco': 'Rua Y'},
#   'message': 'Hospital criado com sucesso',
#   'error': None
# }
```

### 4. Facilidade de Teste
```python
# Testando apenas a lógica de negócio
def test_criar_hospital():
    service = HospitalService()
    resultado = service.criar_hospital("Hospital Teste", "Endereço Teste")
    assert resultado.nome == "Hospital Teste"
```

## Migração Gradual

### Etapa 1: Instalar a Nova Estrutura
```bash
# Já concluída - estrutura criada
```

### Etapa 2: Migrar Código Existente
```python
# Procure por imports antigos
grep -r "from app.crud import" .
grep -r "from app.models import" .

# Substitua pelos novos imports
# app.crud → gem.services
# app.models → gem.models
```

### Etapa 3: Atualizar Scripts e Testes
```python
# Arquivo: populate_specializations.py (antigo)
from app.models import Especializacao
from app.database import db

# Novo equivalente usando serviços
from gem.services import EspecializacaoService
service = EspecializacaoService()
service.popular_especializacoes_iniciais()
```

### Etapa 4: Interface Gráfica (Futuro)
```python
# Com a nova estrutura, a interface será mais limpa
from gem.controllers import HospitalController

class HospitalWindow:
    def __init__(self):
        self.controller = HospitalController()
    
    def criar_hospital(self):
        resposta = self.controller.criar_hospital(self.nome_input.text(), self.endereco_input.text())
        if resposta['success']:
            self.mostrar_sucesso(resposta['message'])
        else:
            self.mostrar_erro(resposta['error'])
```

## Comandos de Verificação

```bash
# Verificar se a estrutura está correta
ls gem/
ls gem/models/
ls gem/repositories/
ls gem/services/
ls gem/controllers/

# Testar imports (quando dependências estiverem instaladas)
python -c "from gem.models import Hospital; print('Models OK')"
python -c "from gem.services import HospitalService; print('Services OK')"
python -c "from gem.controllers import HospitalController; print('Controllers OK')"
```

## Próximos Passos

1. **Instalar dependências**: `pip install -r requirements.txt`
2. **Testar imports**: `python test_structure.py`
3. **Migrar código existente** seguindo os padrões acima
4. **Implementar testes** na pasta `gem/tests/`
5. **Desenvolver interface** usando os controladores