-- db/schema.sql
-- sqlite

-- Tabela para armazenar os Clientes / Proprietários da clínica VetAmigos
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nif TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Tabela de Receitas
CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_consulta INTEGER NOT NULL,
    data_emissao TEXT NOT NULL,
    FOREIGN KEY (id_consulta) REFERENCES consulta(id)
);

-- Tabela de Faturas (relação 1 para 1 estrita com a consulta)
CREATE TABLE IF NOT EXISTS faturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_consulta INTEGER NOT NULL UNIQUE,
    valor_total REAL NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Pendente',
    metodo_pagamento TEXT,
    data_pagamento TEXT,
    FOREIGN KEY (id_consulta) REFERENCES consulta(id)

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