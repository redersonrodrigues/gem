-- Script de criação do banco de dados GEM para SQLite
-- Tabelas: usuario, especializacao, medico, escala_plantonista, escala_sobreaviso, assinatura_escala, audit_log

PRAGMA foreign_keys = ON;

-- 1. Tabela de usuários do sistema
CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    perfil TEXT NOT NULL CHECK (perfil IN ('admin', 'coordenador', 'diretor_tecnico', 'anestesista', 'usuario')),
    status INTEGER NOT NULL DEFAULT 2 -- 1: ativo, 0: inativo
);

-- 2. Tabela de especializações médicas
CREATE TABLE especializacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

-- 3. Tabela de médicos
CREATE TABLE medico (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nome_pj TEXT,
    especializacao_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('ativo', 'inativo')),
    FOREIGN KEY (especializacao_id) REFERENCES especializacao(id) ON DELETE RESTRICT
);

-- 4. Tabela de escala de plantonistas (dois médicos por turno)
CREATE TABLE escala_plantonista (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    turno TEXT NOT NULL CHECK (turno IN ('diurno', 'noturno')),
    medico_0_id INTEGER NOT NULL,
    medico_1_id INTEGER NOT NULL,
    FOREIGN KEY (medico_0_id) REFERENCES medico(id) ON DELETE RESTRICT,
    FOREIGN KEY (medico_1_id) REFERENCES medico(id) ON DELETE RESTRICT,
    CONSTRAINT unq_escala_unique UNIQUE (data, turno, medico_0_id, medico_1_id)
);

-- 5. Tabela de escala de sobreaviso
CREATE TABLE escala_sobreaviso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_inicial DATE NOT NULL,
    data_final DATE NOT NULL,
    medico_id INTEGER NOT NULL,
    especializacao_id INTEGER NOT NULL,
    FOREIGN KEY (medico_id) REFERENCES medico(id) ON DELETE RESTRICT,
    FOREIGN KEY (especializacao_id) REFERENCES especializacao(id) ON DELETE RESTRICT,
    CONSTRAINT unq_sobreaviso UNIQUE (data_inicial, data_final, medico_id, especializacao_id)
);

-- 6. Tabela de assinaturas das escalas (plantonista e sobreaviso)
CREATE TABLE assinatura_escala (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    escala_id INTEGER NOT NULL,
    tipo_escala TEXT NOT NULL CHECK (tipo_escala IN ('plantonista', 'sobreaviso')),
    usuario_id INTEGER NOT NULL,
    papel TEXT NOT NULL CHECK (papel IN ('coordenador', 'diretor_tecnico', 'anestesista')),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE RESTRICT,
    -- Foreign key dinâmica conforme tipo_escala:
    -- Garantir via aplicação: escala_id referencia escala_plantonista.id se tipo_escala='plantonista'
    -- ou escala_sobreaviso.id se tipo_escala='sobreaviso'
    -- Para SQLite, o controle é feito na aplicação.
    CONSTRAINT unq_assinatura UNIQUE (escala_id, tipo_escala, papel)
);

-- 7. Tabela de log de auditoria
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    modelo TEXT NOT NULL,
    operacao TEXT NOT NULL CHECK (operacao IN ('INSERT','UPDATE','DELETE')),
    data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
    dados_anteriores TEXT,
    dados_novos TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE SET NULL
);

-- Índices adicionais para performance
CREATE INDEX idx_medico_especializacao ON medico (especializacao_id);
CREATE INDEX idx_escala_plantonista_data_turno ON escala_plantonista (data, turno);
CREATE INDEX idx_escala_sobreaviso_datas ON escala_sobreaviso (data_inicial, data_final);
CREATE INDEX idx_assinatura_escala_usuario ON assinatura_escala (usuario_id);

-- Views de exemplo
CREATE VIEW vw_medicos_ativos AS
SELECT m.id, m.nome, m.nome_pj, e.nome AS especializacao
  FROM medico m
  JOIN especializacao e ON m.especializacao_id = e.id
 WHERE m.status = 'ativo';

CREATE VIEW vw_escalas_plantonistas AS
SELECT ep.id, ep.data, ep.turno, m0.nome AS medico_0, m1.nome AS medico_1
  FROM escala_plantonista ep
  JOIN medico m0 ON ep.medico_0_id = m0.id
  JOIN medico m1 ON ep.medico_1_id = m1.id;

CREATE VIEW vw_escalas_sobreaviso AS
SELECT es.id, es.data_inicial, es.data_final, m.nome AS medico, e.nome AS especializacao
  FROM escala_sobreaviso es
  JOIN medico m ON es.medico_id = m.id
  JOIN especializacao e ON es.especializacao_id = e.id;

-- Exemplo de trigger para auditoria (para escala_plantonista, similar pode ser criada para outras tabelas)
CREATE TRIGGER trg_audit_escala_plantonista_update
AFTER UPDATE ON escala_plantonista
FOR EACH ROW
BEGIN
  INSERT INTO audit_log (usuario_id, modelo, operacao, dados_anteriores, dados_novos)
  VALUES (
    NULL, -- Preencher via aplicação ou trigger composta
    'escala_plantonista',
    'UPDATE',
    json_object('id', OLD.id, 'data', OLD.data, 'turno', OLD.turno, 'medico_0_id', OLD.medico_0_id, 'medico_1_id', OLD.medico_1_id),
    json_object('id', NEW.id, 'data', NEW.data, 'turno', NEW.turno, 'medico_0_id', NEW.medico_0_id, 'medico_1_id', NEW.medico_1_id)
  );
END;

-- População inicial de exemplos
INSERT INTO especializacao (nome) VALUES ('Clínica Geral'), ('Ortopedia'), ('Anestesiologia');

INSERT INTO usuario (nome, login, senha_hash, perfil, status) VALUES
('Admin', 'admin', 'hash_admin', 'admin', 1),
('Coord. Adm', 'coordenador', 'hash_coord', 'coordenador', 1),
('Dir. Técnico', 'diretor', 'hash_diretor', 'diretor_tecnico', 1),
('Dr. Anestesia', 'anestesia', 'hash_anest', 'anestesista', 1);

-- Exemplo de médicos
INSERT INTO medico (nome, nome_pj, especializacao_id, status) VALUES
('Dr. Fulano', 'PJ Fulano', 1, 'ativo'),
('Dr. Sicrano', 'PJ Sicrano', 2, 'ativo'),
('Dra. Beltrana', 'PJ Beltrana', 3, 'ativo');