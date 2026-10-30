"""src/repositories/medicamento_repository.py"""

from db.connection import get_connection
from src.models.medicamento import Medicamento


class MedicamentoRepository:
    def inserir(self, medicamento: Medicamento) -> Medicamento:
        """Insere um medicamento na base de dados."""
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO medicamentos (nome, tipo, dose, quantidade) VALUES (?, ?, ?, ?)",
                (medicamento.nome, medicamento.tipo, medicamento.dose, medicamento.quantidade)
            )
            medicamento.id = cur.lastrowid
        return medicamento

    def listar_todos(self) -> list[Medicamento]:
        """Devolve todos os medicamentos registados."""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM medicamentos").fetchall()

        medicamentos = [
            Medicamento(
                nome=r["nome"],
                tipo=r["tipo"],
                dose=r["dose"],
                quantidade=r["quantidade"]
            ) for r in rows
        ]

        for i in range(len(rows)):
            medicamentos[i].id = rows[i]["id"]

        return medicamentos

    def obter_por_id(self, id_medicamento: int) -> Medicamento | None:
        """Obtém um medicamento através do seu ID."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM medicamentos WHERE id = ?", (id_medicamento,)
            ).fetchone()

        if row:
            medicamento = Medicamento(
                nome=row["nome"],
                tipo=row["tipo"],
                dose=row["dose"],
                quantidade=row["quantidade"]
            )
            medicamento.id = row["id"]
            return medicamento

        return None

    def atualizar_quantidade(self, id_medicamento: int, quantidade: int):
        """Atualiza a quantidade disponível de um medicamento."""
        with get_connection() as conn:
            conn.execute(
                "UPDATE medicamentos SET quantidade = ? WHERE id = ?",
                (quantidade, id_medicamento)
            )
