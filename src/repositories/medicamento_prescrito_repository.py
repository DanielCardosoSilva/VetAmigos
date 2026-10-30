"""src/repositories/medicamento_prescrito_repository.py"""

from db.connection import get_connection
from src.models.medicamento_prescrito import MedicamentoPrescrito


class MedicamentoPrescritoRepository:
    def inserir(self, medicamento_prescrito: MedicamentoPrescrito) -> MedicamentoPrescrito:
        """Associa um medicamento a uma receita."""
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO medicamentos_prescritos (id_receita, id_medicamento, quantidade, posologia) VALUES (?, ?, ?, ?)",
                (medicamento_prescrito.id_receita, medicamento_prescrito.id_medicamento, medicamento_prescrito.quantidade, medicamento_prescrito.posologia)
            )
            medicamento_prescrito.id = cur.lastrowid
        return medicamento_prescrito

    def listar_por_receita(self, id_receita: int) -> list[MedicamentoPrescrito]:
        """Devolve os medicamentos associados a uma receita."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM medicamentos_prescritos WHERE id_receita = ?",
                (id_receita,)
            ).fetchall()

        medicamentos_prescritos = [
            MedicamentoPrescrito(
                id_receita=r["id_receita"],
                id_medicamento=r["id_medicamento"],
                quantidade=r["quantidade"],
                posologia=r["posologia"]
            ) for r in rows
        ]

        for i in range(len(rows)):
            medicamentos_prescritos[i].id = rows[i]["id"]

        return medicamentos_prescritos
