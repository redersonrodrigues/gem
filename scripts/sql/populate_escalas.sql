-- Limpeza de dados para evitar duplicidade e erros de constraint
DELETE FROM escalas_plantonistas;
DELETE FROM escalas_sobreaviso;

-- Script para popular a tabela de escalas_plantonistas com dados fictícios
-- Supondo IDs de médicos válidos de 1 a 7
INSERT INTO escalas_plantonistas (data, turno, medico1_id, medico2_id) VALUES ('2025-06-21', 'diurno', 1, 2);
INSERT INTO escalas_plantonistas (data, turno, medico1_id, medico2_id) VALUES ('2025-06-21', 'noturno', 3, 4);
INSERT INTO escalas_plantonistas (data, turno, medico1_id, medico2_id) VALUES ('2025-06-22', 'diurno', 5, 6);
INSERT INTO escalas_plantonistas (data, turno, medico1_id, medico2_id) VALUES ('2025-06-22', 'noturno', 7, 1);

-- Script para popular a tabela de escalas_sobreaviso com dados fictícios
-- Supondo IDs de médicos e especializações válidos
INSERT INTO escalas_sobreaviso (data_inicial, data_final, medico1_id, especializacao_id) VALUES ('2025-06-15', '2025-06-21', 2, 2);
INSERT INTO escalas_sobreaviso (data_inicial, data_final, medico1_id, especializacao_id) VALUES ('2025-06-22', '2025-06-30', 4, 6);
