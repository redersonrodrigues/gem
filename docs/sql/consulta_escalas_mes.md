# Consulta: Escalas de plantão e sobreaviso por mês, especialização e médico

## Objetivo

Permitir ao usuário consultar todas as escalas de plantão e sobreaviso de um determinado mês, filtrando por especialização e/ou médico.

## Fluxo de Consulta

1. O usuário informa o mês/ano desejado, podendo filtrar por especialização e/ou médico.
2. O sistema retorna:
   - Todas as escalas de plantão (com data, turno, médicos envolvidos, especialização)
   - Todas as escalas de sobreaviso (com data inicial/final, médico, especialização)
3. O resultado pode ser utilizado para relatórios, conferência de carga horária, auditoria, etc.

## Exemplo de uso (SQL/ORM)

- Buscar todas as escalas de plantão e sobreaviso de junho/2024 para a especialização X e médico Y.

## Parâmetros

- mês/ano (obrigatório)
- especialização (opcional)
- médico (opcional)

## Saída esperada

- Lista de escalas de plantão (data, turno, médicos, especialização)
- Lista de escalas de sobreaviso (data inicial, data final, médico, especialização)

## Observações

- A consulta deve considerar apenas escalas ativas (não excluídas/canceladas).
- O resultado pode ser paginado ou exportado para relatório.

---

# Documentação do fluxo anterior

## Consulta: Médicos disponíveis por especialização e período

### Objetivo

Retornar todos os médicos ativos de uma especialização que não estão escalados (plantão ou sobreaviso) em um determinado período.

### Fluxo

1. Usuário informa especialização, data inicial e data final.
2. O sistema busca todos os médicos ativos daquela especialização.
3. Exclui da lista os médicos que já estão escalados em plantão ou sobreaviso no período informado.
4. Retorna a lista de médicos disponíveis.

### Implementação

- Função utilitária: `medicos_disponiveis_por_especializacao_periodo(db, especializacao_id, data_inicio, data_fim)`
- Testes automatizados de integração garantem a precisão do resultado.

### Observações

- Considera apenas médicos com status 'ativo'.
- Consulta eficiente via SQLAlchemy, utilizando subqueries para escalas de plantão e sobreaviso.
- Documentação e exemplos de uso disponíveis em `app/core/consulta_medicos_disponiveis.py` e `tests/integration/test_consultas.py`.

---

# Consulta: Médicos com maior número de plantões em determinado período

## Objetivo

Listar os médicos que mais realizaram plantões em um intervalo de datas, ordenando do maior para o menor número de plantões.

## Fluxo de Consulta

1. O usuário informa a data inicial e final do período desejado (e opcionalmente a especialização).
2. O sistema retorna:
   - Lista de médicos, com nome, especialização e total de plantões realizados no período.
   - Ordenação do maior para o menor número de plantões.
3. O resultado pode ser utilizado para relatórios de produtividade, premiações, auditoria, etc.

## Exemplo de uso (SQL/ORM)

- Buscar os médicos com mais plantões entre 01/06/2024 e 30/06/2024.

## Parâmetros

- data_inicial (obrigatório)
- data_final (obrigatório)
- especializacao_id (opcional)

## Saída esperada

- Lista de médicos (id, nome, especialização, total_plantao)

## Observações

- Considera apenas médicos ativos.
- Consulta eficiente via SQLAlchemy, utilizando agregação (COUNT) e ordenação decrescente.
- Testes automatizados de integração garantem a precisão do resultado.

---

# Consulta: Médicos sem escalas atribuídas em um intervalo de datas

## Objetivo

Listar os médicos ativos que não possuem nenhuma escala (plantão ou sobreaviso) em um intervalo de datas.

## Fluxo de Consulta

1. O usuário informa a data inicial e final do período desejado (e opcionalmente a especialização).
2. O sistema retorna:
   - Lista de médicos ativos que não estão em nenhuma escala de plantão ou sobreaviso no período.
3. O resultado pode ser utilizado para identificar disponibilidade, evitar ociosidade, etc.

## Exemplo de uso (SQL/ORM)

- Buscar médicos sem escalas entre 01/06/2024 e 30/06/2024.

## Parâmetros

- data_inicial (obrigatório)
- data_final (obrigatório)
- especializacao_id (opcional)

## Saída esperada

- Lista de médicos (id, nome, especialização)

## Observações

- Considera apenas médicos com status 'ativo'.
- Consulta eficiente via SQLAlchemy, utilizando subqueries para plantão e sobreaviso.
- Testes automatizados de integração garantem a precisão do resultado.

---

# Consulta: Cobertura de especialidades por turno (identificar lacunas)

## Objetivo

Identificar especializações e turnos sem médicos escalados (lacunas) em um período.

## Fluxo de Consulta

1. O usuário informa a data inicial e final do período desejado.
2. O sistema retorna:
   - Lista de especializações e turnos (por dia) sem plantonista escalado.
3. O resultado pode ser utilizado para identificar riscos de falta de cobertura, planejamento, etc.

## Exemplo de uso (SQL/ORM)

- Buscar lacunas de cobertura entre 10/06/2024 e 11/06/2024.

## Parâmetros

- data_inicial (obrigatório)
- data_final (obrigatório)

## Saída esperada

- Lista de tuplas (especializacao_id, nome_especializacao, data, turno) sem plantonista escalado

## Observações

- Considera todos os turnos (diurno, noturno) para cada especialização e dia.
- Consulta eficiente via SQLAlchemy, iterando por especialização, data e turno.
- Testes automatizados de integração garantem a precisão do resultado.

---

## Consulta: Médicos inativos ou afastados em determinado período

### Objetivo

Listar médicos que estão inativos (status = 'inativo') ou afastados (sem escalas atribuídas) em um intervalo de datas.

### Parâmetros

- data_inicial (obrigatório)
- data_final (obrigatório)

### Critérios

- Inativo: médico com status 'inativo' no cadastro
- Afastado: médico ativo que não possui escala de plantão nem sobreaviso no período

### Exemplo de uso (ORM)

```python
resultado = medicos_inativos_afastados(session, data_inicio, data_fim)
print(resultado['inativos'])  # lista de médicos inativos
print(resultado['afastados'])  # lista de médicos afastados no período
```

### Observações

- Útil para relatórios de RH, controle de afastamentos e auditoria de escalas.
- Pode ser expandida para considerar tipos de afastamento/documentação.

---

## Consulta: Escalas com conflitos de horário ou sobreposição de médicos

### Objetivo

Identificar escalas de plantão e sobreaviso com conflitos de horário para o mesmo médico, incluindo sobreposição de plantões, sobreavisos e plantão x sobreaviso.

### Parâmetros

- data_inicial (obrigatório)
- data_final (obrigatório)

### Critérios

- Plantão x Plantão: (não permitido pelo banco, mas pode ser validado na interface)
- Sobreaviso x Sobreaviso: interseção de datas para o mesmo médico
- Plantão x Sobreaviso: plantão dentro do período de sobreaviso do mesmo médico

### Exemplo de uso (ORM)

```python
conflitos = escalas_com_conflitos(session, data_inicio, data_fim)
for c in conflitos:
    print(c)
```

### Observações

- Útil para evitar erros de escala, sobrecarga e garantir conformidade.
- O resultado pode ser exibido em tela de conferência ou exportado para relatório.

---

## Relatório: Escala mensal de plantonistas (PDF/CSV)

### Objetivo

Gerar relatório mensal dos plantonistas, exportável em PDF e CSV, contendo data, turno e nome do médico.

### Parâmetros

- ano (obrigatório)
- mês (obrigatório)

### Fluxo

1. Consulta os plantões do mês informado.
2. Gera lista com data, turno e médico.
3. Exporta para PDF (ReportLab) e CSV (csv.DictWriter).

### Exemplo de uso

```python
dados = dados_escala_plantonistas(session, 2024, 6)
exportar_csv(dados, 'relatorio.csv')
exportar_pdf(dados, 'relatorio.pdf')
```

### Observações

- O layout do PDF pode ser customizado conforme identidade visual.
- O CSV pode ser importado em planilhas para análise.

---

# Relatório: Escala mensal de sobreaviso (PDF/CSV)

## Objetivo

Gerar um relatório mensal de escalas de sobreaviso, agrupando por especialização e médico, com exportação em PDF e CSV.

## Parâmetros

- Ano/mês de referência (obrigatório)

## Saída esperada

- Lista de períodos de sobreaviso (data inicial, data final, médico, especialização)
- Exportação em PDF e CSV

## Exemplo de uso (ORM)

```python
from app.core.relatorio_escala_sobreaviso import consultar_sobreaviso_mes, exportar_csv, exportar_pdf

dados = consultar_sobreaviso_mes(session, 2024, 6)
exportar_csv(dados, 'relatorio_sobreaviso.csv')
exportar_pdf(dados, 'relatorio_sobreaviso.pdf')
```

## Observações

- O relatório considera apenas escalas ativas.
- O layout do PDF segue padrão simples, com colunas: data_inicial, data_final, médico, especialização.
- O CSV segue o mesmo padrão de colunas.
- O relatório é útil para conferência, auditoria e planejamento de sobreavisos.
