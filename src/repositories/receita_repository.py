"""src/repositories/receita_repository.py"""

from datetime import date
from src.models.receita import Receita
from db.connection import get_connection


class ReceitaRepository:
    def inserir(self, receita: Receita) -> Receita:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO receitas (id_consulta, data_emissao) VALUES (?, ?)",
                (receita.id_consulta, receita.data_emissao.isoformat())
            )
            receita.id = cur.lastrowid

        return receita

    def listar_por_consulta(self, id_consulta: int) -> list[Receita]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM receitas WHERE id_consulta = ?", (id_consulta,)
            ).fetchall()

        receitas = [
            Receita(
                id_consulta=r["id_consulta"],
                data_emissao=date.fromisoformat(r["data_emissao"])
            )
            for r in rows
        ]

        for i in range(len(rows)):
            receitas[i].id = rows[i]["id"]

        return receitas

    def obter_por_id(self, id_receita: int) -> Receita | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM receitas WHERE id = ?", (id_receita,)
            ).fetchone()

        if row:
            receita = Receita(
                id_consulta=row["id_consulta"],
                data_emissao=date.fromisoformat(row["data_emissao"])
            )
            receita.id = row["id"]
            return receita

        return None
    