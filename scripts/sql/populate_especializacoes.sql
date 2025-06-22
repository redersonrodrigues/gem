-- Limpeza de dados para evitar duplicidade e erros de constraint
DELETE FROM escalas_plantonistas;
DELETE FROM escalas_sobreaviso;
DELETE FROM medicos;
DELETE FROM especializacoes;

-- Script para popular a tabela de especializações com dados iniciais
INSERT INTO especializacoes (nome) VALUES ('PLANTONISTA');
INSERT INTO especializacoes (nome) VALUES ('ANESTESISTA');
INSERT INTO especializacoes (nome) VALUES ('CLÍNICA CIRÚRGICA');
INSERT INTO especializacoes (nome) VALUES ('CLÍNICA MÉDICA');
INSERT INTO especializacoes (nome) VALUES ('G.O.');
INSERT INTO especializacoes (nome) VALUES ('ORTOPEDIA');
INSERT INTO especializacoes (nome) VALUES ('PEDIATRIA');
