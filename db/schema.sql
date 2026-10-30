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
);