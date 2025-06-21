# Estrutura de tabelas e campos do banco de dados gem.db

## Tabela: especializacoes

- id (INTEGER, PK, autoincremento)
- nome (TEXT, único, não nulo)

## Tabela: medicos

- id (INTEGER, PK, autoincremento)
- nome (TEXT, não nulo)
- nome_pj (TEXT, opcional)
- especializacao_id (INTEGER, FK para especializacoes.id, não nulo)
- status (TEXT, não nulo, valores: 'ativo', 'inativo')

## Tabela: escalas_plantonistas

- id (INTEGER, PK, autoincremento)
- data (DATE, não nulo)
- turno (TEXT, não nulo, valores: 'diurno', 'noturno')
- medico1_id (INTEGER, FK para medicos.id, não nulo)
- medico2_id (INTEGER, FK para medicos.id, opcional)

## Tabela: escalas_sobreaviso

- id (INTEGER, PK, autoincremento)
- data_inicial (DATE, não nulo)
- data_final (DATE, não nulo)
- medico1_id (INTEGER, FK para medicos.id, não nulo)
- especializacao_id (INTEGER, FK para especializacoes.id, não nulo)

---

Obs: Esta estrutura segue o checklist e os requisitos do projeto, incluindo as relações e restrições necessárias para garantir integridade referencial e normalização.
