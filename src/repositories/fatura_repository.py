"""src/repositories/fatura_repository.py"""

from datetime import date
from src.models.fatura import Fatura
from db.connection import get_connection


class FaturaRepository:
    def inserir(self, fatura: Fatura) -> Fatura:
        # Inserir uma nova fatura na base de dados.
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
        # Consultar uma fatura associada a uma consulta.
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

    def _converter_linha(self, row):
        # Converter uma linha SQLite num objeto Fatura.
        if row is None:
            return None

        fatura = Fatura(
            id_consulta=row["id_consulta"],
            valor_total=row["valor_total"],
            estado=row["estado"],
            metodo_pagamento=row["metodo_pagamento"],
            data_pagamento=date.fromisoformat(row["data_pagamento"]) if row["data_pagamento"] else None
        )
        fatura.id = row["id"]
        return fatura

    def listar_todas(self):
        # Obter todas as faturas, incluindo pendentes e anuladas.
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM faturas ORDER BY id DESC"
            ).fetchall()

        return [self._converter_linha(row) for row in rows]

    def obter_por_id(self, identificador):
        # Procurar uma fatura pelo seu identificador.
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM faturas WHERE id = ?",
                (identificador,)
            ).fetchone()

        return self._converter_linha(row)

    def atualizar_estado(self, identificador, estado, metodo_pagamento, data_pagamento):
        # Atualizar o estado e os dados de pagamento de uma fatura.
        with get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE faturas
                SET estado = ?, metodo_pagamento = ?, data_pagamento = ?
                WHERE id = ?
                """,
                (
                    estado,
                    metodo_pagamento,
                    data_pagamento.isoformat() if data_pagamento else None,
                    identificador
                )
            )

            return cur.rowcount > 0
