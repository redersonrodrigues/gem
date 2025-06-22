-- Limpeza de dados para evitar duplicidade e erros de constraint
DELETE FROM escalas_plantonistas;
DELETE FROM escalas_sobreaviso;
DELETE FROM medicos;

-- Script para popular a tabela de médicos com dados fictícios
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dr. João Silva', 'João Silva ME', 1, 'ativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dra. Maria Souza', 'Maria Souza LTDA', 2, 'ativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dr. Carlos Pereira', 'Carlos Pereira EPP', 3, 'inativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dra. Ana Lima', 'Ana Lima ME', 4, 'ativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dr. Pedro Rocha', 'Pedro Rocha ME', 5, 'ativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dra. Fernanda Alves', 'Fernanda Alves LTDA', 6, 'ativo');
INSERT INTO medicos (nome, nome_pj, especializacao_id, status) VALUES ('Dr. Lucas Martins', 'Lucas Martins ME', 7, 'ativo');
