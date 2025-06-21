-- Documentação das views SQL criadas para facilitar consultas comuns no banco de dados:
--
-- 1. vw_escalas_por_medico:
--    - Mostra todas as escalas (plantonista e sobreaviso) com informações dos médicos, tipo, datas e especialização.
--    - Útil para relatórios de agenda de médicos e acompanhamento de plantões.
--    - Colunas: escala_id, tipo, data, turno, medico_1, medico_2, especializacao, data_final
--
-- 2. vw_escalas_por_especializacao:
--    - Lista escalas de sobreaviso agrupadas por especialização, com datas e médico responsável.
--    - Útil para consultas rápidas por especialidade e planejamento de escalas.
--    - Colunas: especializacao, escala_id, data_inicial, data_final, medico
--
-- 3. vw_medicos_ativos_especializacoes:
--    - Lista todos os médicos ativos e suas especializações.
--    - Útil para filtros de cadastro, seleção em formulários e relatórios administrativos.
--    - Colunas: medico_id, medico, especializacao
--
-- As views estão definidas em scripts/sql/views.sql e são aplicadas automaticamente pelo script apply_views.py.
-- Para testar, utilize scripts/sql/test_views.py ou consultas SQL diretas.

-- View 1: Escalas por Médico (plantonista e sobreaviso)
CREATE VIEW IF NOT EXISTS vw_escalas_por_medico AS
SELECT e.id AS escala_id, 'plantonista' AS tipo, e.data, e.turno, m1.nome AS medico_1, m2.nome AS medico_2, NULL AS especializacao, NULL AS data_final
FROM escalas_plantonistas e
JOIN medicos m1 ON e.medico1_id = m1.id
JOIN medicos m2 ON e.medico2_id = m2.id
UNION ALL
SELECT s.id AS escala_id, 'sobreaviso' AS tipo, s.data_inicial AS data, NULL AS turno, m.nome AS medico_1, NULL AS medico_2, esp.nome AS especializacao, s.data_final
FROM escalas_sobreaviso s
JOIN medicos m ON s.medico1_id = m.id
JOIN especializacoes esp ON s.especializacao_id = esp.id;

-- View 2: Escalas por Especialização
CREATE VIEW IF NOT EXISTS vw_escalas_por_especializacao AS
SELECT esp.nome AS especializacao, s.id AS escala_id, s.data_inicial, s.data_final, m.nome AS medico
FROM escalas_sobreaviso s
JOIN especializacoes esp ON s.especializacao_id = esp.id
JOIN medicos m ON s.medico1_id = m.id;

-- View 3: Médicos ativos e suas especializações
CREATE VIEW IF NOT EXISTS vw_medicos_ativos_especializacoes AS
SELECT m.id AS medico_id, m.nome AS medico, esp.nome AS especializacao
FROM medicos m
LEFT JOIN especializacoes esp ON m.especializacao_id = esp.id
WHERE m.status = 'ativo';
