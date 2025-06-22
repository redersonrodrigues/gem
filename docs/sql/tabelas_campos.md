# Estrutura de tabelas e campos do banco de dados gem.db

## Tabela: especializacoes

- id (INTEGER, PK, autoincremento)
- nome (TEXT, único, não nulo)
- version (INTEGER, não nulo, default=1)

**Relações:**

- Um para muitos com `medicos` (especializacoes.id → medicos.especializacao_id)

## Tabela: medicos

- id (INTEGER, PK, autoincremento)
- nome (TEXT, não nulo)
- nome_pj (TEXT, opcional)
- especializacao_id (INTEGER, FK para especializacoes.id, não nulo)
- status (TEXT, não nulo, valores: 'ativo', 'inativo', 'afastado')
- version (INTEGER, não nulo, default=1)

**Constraints:**

- UNIQUE (nome, especializacao_id)

**Relações:**

- Muitos para um com `especializacoes`
- Um para muitos com `escalas_plantonistas` (medico1_id, medico2_id)
- Um para muitos com `escalas_sobreaviso` (medico1_id)

## Tabela: escalas_plantonistas

- id (INTEGER, PK, autoincremento)
- data (DATE, não nulo)
- turno (TEXT, não nulo, valores: 'diurno', 'noturno')
- medico1_id (INTEGER, FK para medicos.id, não nulo)
- medico2_id (INTEGER, FK para medicos.id, opcional)
- version (INTEGER, não nulo, default=1)

**Constraints:**

- UNIQUE (data, turno)

**Relações:**

- Muitos para um com `medicos` (medico1_id, medico2_id)

## Tabela: escalas_sobreaviso

- id (INTEGER, PK, autoincremento)
- data_inicial (DATE, não nulo)
- data_final (DATE, não nulo)
- medico1_id (INTEGER, FK para medicos.id, não nulo)
- especializacao_id (INTEGER, FK para especializacoes.id, não nulo)
- version (INTEGER, não nulo, default=1)

**Constraints:**

- UNIQUE (data_inicial, data_final, medico1_id, especializacao_id)

**Relações:**

- Muitos para um com `medicos` e `especializacoes`

## Tabela: audit_log

- id (INTEGER, PK, autoincremento)
- usuario (TEXT)
- data_hora (TEXT, ISO datetime)
- operacao (TEXT)
- tabela (TEXT)
- registro_id (INTEGER)
- dados_anteriores (TEXT)
- dados_novos (TEXT)

**Descrição:**

- Log de auditoria de operações CRUD.

## Tabela: historico_versao

- id (INTEGER, PK, autoincremento)
- tabela (TEXT, não nulo)
- registro_id (INTEGER, não nulo)
- versao (INTEGER, não nulo)
- usuario (TEXT)
- data_hora (DATETIME, default=UTC now)
- dados (TEXT) # JSON serializado do estado do registro

**Descrição:**

- Histórico de versões de registros para rastreamento de alterações.

---

Obs: Esta estrutura foi gerada automaticamente a partir dos modelos ORM reais do sistema, incluindo versionamento, auditoria e histórico, e reflete fielmente as constraints e relações do banco.
