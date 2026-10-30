# src/repositories/fatura_repository.py
from datetime import date
from src.models.fatura import Fatura
from db.connection import get_connection

class FaturaRepository:
    def inserir(self, fatura: Fatura) -> Fatura:
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO faturas (id_consulta, valor_total, estado, metodo_pagamento, data_pagamento) 
                   VALUES (?, ?, ?, ?, ?)""",
                (fatura.id_consulta, fatura.valor_total, fatura.estado, 
                 fatura.metodo_pagamento, str(fatura.data_pagamento) if fatura.data_pagamento else None)
            )
            fatura.id = cur.lastrowid
        return fatura

    def obter_por_consulta(self, id_consulta: int) -> Fatura | None:
        with get_connection() as conn:
            r = conn.execute("SELECT * FROM faturas WHERE id_consulta = ?", (id_consulta,)).fetchone()
            if r:
                return Fatura(
                    id_consulta=r["id_consulta"],
                    valor_total=r["valor_total"],
                    estado=r["estado"],
                    metodo_pagamento=r["metodo_pagamento"],
                    data_pagamento=date.fromisoformat(r["data_pagamento"]) if r["data_pagamento"] else None,
                    id=r["id"]
                )
        return None