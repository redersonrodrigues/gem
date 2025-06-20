CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> e26c95c996d8

CREATE TABLE escala (
    id INTEGER NOT NULL, 
    data_inicio DATE NOT NULL, 
    data_fim DATE NOT NULL, 
    tipo VARCHAR(50) NOT NULL, 
    medico_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(medico_id) REFERENCES medico (id)
);

CREATE TABLE escala_plantonista (
    id INTEGER NOT NULL, 
    turno VARCHAR(50) NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(id) REFERENCES escala (id)
);

CREATE TABLE escala_sobreaviso (
    id INTEGER NOT NULL, 
    especialidade_id INTEGER NOT NULL, 
    PRIMARY KEY (id), 
    FOREIGN KEY(id) REFERENCES escala (id), 
    FOREIGN KEY(especialidade_id) REFERENCES especializacao (id)
);

INSERT INTO alembic_version (version_num) VALUES ('e26c95c996d8') RETURNING version_num;

