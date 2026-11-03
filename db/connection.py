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
