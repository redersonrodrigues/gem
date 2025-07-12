# GEM - Aplicação Python MVC

## Descrição

Aplicação Python seguindo o padrão arquitetural MVC (Model-View-Controller) com estrutura modular e organizada.

## Estrutura do Projeto

```text
gem/
├── main.py                          # Arquivo principal da aplicação
├── README.md                        # Documentação do projeto
├── app/                            # Diretório principal da aplicação
│   ├── app.yaml                    # Arquivo de configuração da aplicação
│   ├── controllers/                # Camada de controle (Controllers)
│   │   ├── doctor/                 # Controladores relacionados a médicos
│   │   │   └── doctor_controller.py
│   │   └── user/                   # Controladores relacionados a usuários
│   │       └── user_controller.py
│   ├── models/                     # Camada de modelo (Models)
│   │   ├── doctor/                 # Modelos relacionados a médicos
│   │   │   ├── doctor.py          # Entidade Doctor
│   │   │   ├── doctor_mapper.py   # Mapeamento de dados Doctor
│   │   │   └── doctor_repository.py # Repositório Doctor
│   │   └── user/                   # Modelos relacionados a usuários
│   │       ├── user.py            # Entidade User
│   │       ├── user_mapper.py     # Mapeamento de dados User
│   │       └── user_repository.py # Repositório User
│   └── views/                      # Camada de visualização (Views)
│       ├── doctor/                 # Views relacionadas a médicos
│       │   ├── doctor_form.html   # Formulário de médico
│       │   └── doctor_list.html   # Listagem de médicos
│       └── user/                   # Views relacionadas a usuários
│           ├── user_form.html     # Formulário de usuário
│           └── user_list.html     # Listagem de usuários
└── lib/                           # Biblioteca de componentes base
    ├── control/                   # Componentes de controle
    │   ├── front_controller.py   # Controlador frontal
    │   └── page_controller.py    # Controlador de página
    ├── core/                      # Núcleo da aplicação
    │   ├── application_loader.py # Carregador da aplicação
    │   ├── entity_base.py        # Classe base para entidades
    │   └── library_loader.py     # Carregador de bibliotecas
    ├── db/                        # Componentes de banco de dados
    │   ├── adapter.py            # Adaptador de banco
    │   ├── connection_factory.py # Fábrica de conexões
    │   ├── criteria.py           # Critérios de consulta
    │   ├── mapper.py             # Mapeador base
    │   ├── repository.py         # Repositório base
    │   ├── strategy.py           # Estratégias de persistência
    │   └── transaction.py        # Gerenciamento de transações
    ├── log/                       # Sistema de logging
    │   ├── logger.py             # Logger principal
    │   └── logger_mixin.py       # Mixin para logging
    ├── session/                   # Gerenciamento de sessão
    │   └── session.py            # Classe de sessão
    ├── traits/                    # Traits e características
    │   └── traits.py             # Implementação de traits
    ├── validation/                # Sistema de validação
    │   └── validation.py         # Validadores
    └── widget/                    # Componentes de interface
        └── widget_base.py        # Classe base para widgets
```

## Arquitetura

### Padrão MVC

- **Models** (`app/models/`): Contém as entidades de negócio, repositórios e mapeadores
- **Views** (`app/views/`): Templates HTML para renderização da interface
- **Controllers** (`app/controllers/`): Lógica de controle e manipulação de requisições

### Biblioteca Base (`lib/`)

- **Control**: Controladores frontais e de página
- **Core**: Núcleo da aplicação com carregadores e classes base
- **DB**: Camada de acesso a dados com padrões Repository e Mapper
- **Log**: Sistema de logging integrado
- **Session**: Gerenciamento de sessões
- **Traits**: Implementação de características reutilizáveis
- **Validation**: Sistema de validação de dados
- **Widget**: Componentes de interface reutilizáveis

## Módulos Principais

### Doctor

- Gerenciamento de informações de médicos
- CRUD completo com formulários e listagens

### User

- Gerenciamento de usuários do sistema
- CRUD completo com formulários e listagens

## Como Executar

```bash
python main.py
```

## Configuração

A configuração da aplicação está definida no arquivo `app/app.yaml`.

## Tecnologias Utilizadas

- Python
- Padrão MVC
- Sistema de templates HTML
- Arquitetura modular
- Padrões Repository e Mapper
- Sistema de logging integrado
