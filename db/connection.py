"""db/connection.py"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "vetamigos.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def inicializar_bd():
    schema = Path(__file__).parent / "schema.sql"

    with get_connection() as conn:
        conn.executescript(schema.read_text(encoding="utf-8"))

        colunas = conn.execute(
            "PRAGMA table_info(funcionarios)"
        ).fetchall()

        nomes_colunas = {
            coluna["name"] for coluna in colunas
        }

        if "ativo" not in nomes_colunas:
            conn.execute(
                """
                ALTER TABLE funcionarios
                ADD COLUMN ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0, 1))
                """
            )

        # Migração incremental, preservando os dados existentes.
        colunas_consulta = {c["name"] for c in conn.execute("PRAGMA table_info(consultas)")}
        for nome, definicao in (
            ("motivo", "TEXT NOT NULL DEFAULT ''"),
            ("sumario", "TEXT NOT NULL DEFAULT ''"),
            ("data_conclusao", "TEXT"),
        ):
            if nome not in colunas_consulta:
                conn.execute(f"ALTER TABLE consultas ADD COLUMN {nome} {definicao}")
