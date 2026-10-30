"""src/repositories/fatura_repository.py"""

from datetime import date
from src.models.fatura import Fatura
from db.connection import get_connection


class FaturaRepository:
    def inserir(self, fatura: Fatura) -> Fatura:
        with get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO faturas (
                    id_consulta, valor_total, estado,
                    metodo_pagamento, data_pagamento
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    fatura.id_consulta,
                    fatura.valor_total,
                    fatura.estado,
                    fatura.metodo_pagamento,
                    fatura.data_pagamento.isoformat() if fatura.data_pagamento else None
                )
            )
            fatura.id = cur.lastrowid

        return fatura

    def obter_por_consulta(self, id_consulta: int) -> Fatura | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM faturas WHERE id_consulta = ?", (id_consulta,)
            ).fetchone()

        if row:
            fatura = Fatura(
                id_consulta=row["id_consulta"],
                valor_total=row["valor_total"],
                estado=row["estado"],
                metodo_pagamento=row["metodo_pagamento"],
                data_pagamento=date.fromisoformat(row["data_pagamento"]) if row["data_pagamento"] else None
            )
            fatura.id = row["id"]
            return fatura

        return None