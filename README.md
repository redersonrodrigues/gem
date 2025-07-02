# GEM - Sistema de Gestão de Escalas Médicas

## Descrição

O GEM (Gestão de Escalas Médicas) é uma aplicação desktop Python desenvolvida seguindo os padrões MVC (Model-View-Controller), OOP (Programação Orientada a Objetos) e Design Patterns para facilitar a manutenção, escalabilidade e qualidade do código.

## Estrutura do Projeto

```
gem/
├── controllers/          # Controladores (Lógica de apresentação)
│   ├── __init__.py
│   ├── base_controller.py
│   ├── hospital_controller.py
│   └── medico_controller.py
├── models/              # Modelos de dados (Entidades)
│   ├── __init__.py
│   ├── base_models.py
│   └── escala_models.py
├── views/               # Views (Interface de usuário)
│   └── __init__.py
├── repositories/        # Repositórios (Acesso a dados)
│   ├── __init__.py
│   ├── base_repository.py
│   ├── hospital_repository.py
│   ├── medico_repository.py
│   └── especializacao_repository.py
├── services/           # Serviços (Lógica de negócio)
│   ├── __init__.py
│   ├── hospital_service.py
│   ├── medico_service.py
│   └── especializacao_service.py
├── utils/              # Utilitários
│   ├── __init__.py
│   └── database.py
├── tests/              # Testes
│   └── __init__.py
├── assets/             # Recursos estáticos
├── docs/               # Documentação
├── alembic/            # Migrações do banco de dados
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── app.py              # Configuração da aplicação Flask
└── __init__.py
requirements.txt        # Dependências
main.py                # Ponto de entrada da aplicação
```

## Padrões Implementados

### 1. MVC (Model-View-Controller)
- **Models**: Representam as entidades de dados (`gem/models/`)
- **Views**: Interface de usuário (a ser implementada em `gem/views/`)
- **Controllers**: Lógica de apresentação e coordenação (`gem/controllers/`)

### 2. Repository Pattern
- Abstração do acesso a dados
- Separação clara entre lógica de negócio e persistência
- Base repository com operações CRUD genéricas

### 3. Service Layer Pattern
- Lógica de negócio encapsulada em serviços
- Validações e regras de negócio centralizadas
- Reutilização de código entre diferentes controladores

### 4. Strategy Pattern
- Implementado nos modelos de Escala
- Permite diferentes estratégias para tipos de escala (Plantonista, Sobreaviso)

## Principais Entidades

### Hospital
- **Atributos**: id, nome, endereco
- **Relacionamentos**: Pode ter vários médicos

### Médico
- **Atributos**: id, nome
- **Relacionamentos**: 
  - Muitas especializações (N:N)
  - Várias escalas (1:N)

### Especialização
- **Atributos**: id, nome
- **Relacionamentos**: Muitos médicos (N:N)

### Escala
- **Tipos**: Plantonista, Sobreaviso
- **Atributos**: id, data_inicio, data_fim, tipo, medico_id
- **Padrão Strategy**: Diferentes comportamentos por tipo

## Tecnologias Utilizadas

- **Python 3.8+**
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **Flask-Migrate**: Migrações de banco
- **SQLite**: Banco de dados (desenvolvimento)
- **PyQt5**: Interface desktop (futuro)
- **pytest**: Testes unitários

## Instalação e Execução

### Pré-requisitos
```bash
python -m pip install -r requirements.txt
```

### Executar a aplicação
```bash
python main.py
```

### Executar migrações
```bash
cd gem/alembic
alembic upgrade head
```

## Uso da API

### Exemplo de uso dos controladores:

```python
from gem.controllers import HospitalController, MedicoController

# Controlador de Hospital
hospital_controller = HospitalController()

# Criar hospital
resultado = hospital_controller.criar_hospital("Hospital São Paulo", "Rua A, 123")
print(resultado)  # {'success': True, 'data': {...}, 'message': '...'}

# Listar hospitais
hospitais = hospital_controller.listar_hospitais()

# Controlador de Médico
medico_controller = MedicoController()

# Criar médico
medico = medico_controller.criar_medico("Dr. João Silva")
```

## Testes

Os testes devem ser implementados na pasta `gem/tests/`. Estrutura sugerida:

```
tests/
├── test_models/
├── test_repositories/
├── test_services/
├── test_controllers/
└── conftest.py
```

## Contribuição

1. Siga os padrões estabelecidos na arquitetura
2. Implemente testes para novas funcionalidades
3. Mantenha a documentação atualizada
4. Use type hints quando possível
5. Siga as convenções PEP 8

## Próximas Implementações

- [ ] Interface gráfica com PyQt5
- [ ] Testes unitários completos
- [ ] API REST com Flask
- [ ] Autenticação e autorização
- [ ] Relatórios em PDF
- [ ] Dashboard analítico

## Licença

Este projeto está sob licença MIT.