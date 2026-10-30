# src/repositories/receita_repository.py
from datetime import date
from src.models.receita import Receita
from db.connection import get_connection

class ReceitaRepository:
    def inserir(self, receita: Receita) -> Receita:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO receitas (id_consulta, data_emissao) VALUES (?, ?)",
                (receita.id_consulta, str(receita.data_emissao))
            )
            receita.id = cur.lastrowid
        return receita

    def listar_por_consulta(self, id_consulta: int) -> list[Receita]:
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM receitas WHERE id_consulta = ?", (id_consulta,)).fetchall()
        return [
            Receita(
                id_consulta=r["id_consulta"],
                data_emissao=date.fromisoformat(r["data_emissao"]),
                id=r["id"]
            ) for r in rows
        ]