-- db/schema.sql
-- sqlite

CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal INTEGER NOT NULL,
    cedula_profissional TEXT NOT NULL,
    horario TEXT NOT NULL,
    diagnostico TEXT NOT NULL DEFAULT '',
    tratamento TEXT NOT NULL DEFAULT '',
    custo REAL NOT NULL DEFAULT 0.0,
    peso_registado REAL,
    estado TEXT NOT NULL DEFAULT 'Agendada',

    FOREIGN KEY (id_animal)
        REFERENCES animais(id),

    FOREIGN KEY (cedula_profissional)
        REFERENCES medicos_veterinarios(cedula_profissional)
);