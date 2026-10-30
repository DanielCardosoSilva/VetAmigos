
-- db/schema.sql
-- SQLite

-- =============================================
-- CLIENTES
-- =============================================

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nif TEXT NOT NULL UNIQUE,
    telefone TEXT NOT NULL,
    email TEXT NOT NULL
);

-- =============================================
-- FUNCIONARIOS
-- =============================================

CREATE TABLE IF NOT EXISTS funcionarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    nome_utilizador TEXT NOT NULL UNIQUE,
    palavra_passe_hash TEXT NOT NULL,
    tipo TEXT NOT NULL,
    cedula_profissional TEXT UNIQUE
);

-- =============================================
-- ANIMAIS
-- =============================================

CREATE TABLE IF NOT EXISTS animais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    especie TEXT NOT NULL,
    data_nasc TEXT NOT NULL,
    peso_animal REAL NOT NULL,
    nif_cliente TEXT NOT NULL,

    FOREIGN KEY (nif_cliente)
        REFERENCES clientes(nif)
);

-- =============================================
-- CONSULTAS
-- =============================================

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
        REFERENCES funcionarios(cedula_profissional)
);

-- =============================================
-- RECEITAS
-- =============================================

CREATE TABLE IF NOT EXISTS receitas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_consulta INTEGER NOT NULL,
    data_emissao TEXT NOT NULL,

    FOREIGN KEY (id_consulta)
        REFERENCES consultas(id)
);

-- =============================================
-- FATURAS
-- =============================================

CREATE TABLE IF NOT EXISTS faturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_consulta INTEGER NOT NULL UNIQUE,
    valor_total REAL NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Pendente',
    metodo_pagamento TEXT,
    data_pagamento TEXT,

    FOREIGN KEY (id_consulta)
        REFERENCES consultas(id)
);

-- =============================================
-- MEDICAMENTOS
-- =============================================

CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    tipo TEXT NOT NULL,
    dose TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0
);

-- =============================================
-- MEDICAMENTOS PRESCRITOS
-- =============================================

CREATE TABLE IF NOT EXISTS medicamentos_prescritos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_receita INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    posologia TEXT NOT NULL,

    FOREIGN KEY (id_receita)
        REFERENCES receitas(id),

    FOREIGN KEY (id_medicamento)
        REFERENCES medicamentos(id)
);

-- =============================================
-- REGISTOS DE VACINAS
-- =============================================

CREATE TABLE IF NOT EXISTS registovacina (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_animal INTEGER NOT NULL,
    nome_vacina TEXT NOT NULL,
    data_administracao TEXT NOT NULL,
    data_proxima_dose TEXT,

    FOREIGN KEY (id_animal)
        REFERENCES animais(id)
);
