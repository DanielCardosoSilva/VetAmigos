from db.connection import get_connection
from src.models.consulta import Consulta
from datetime import datetime


class ConsultaRepository:

    def agendar(self, consulta):
        with get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO consultas (
                    id_animal,
                    cedula_profissional,
                    horario,
                    diagnostico,
                    tratamento,
                    custo,
                    peso_registado,
                    estado
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    consulta.id_animal,
                    consulta.cedula_profissional,
                    consulta.horario.isoformat(sep=" "),
                    consulta.diagnostico,
                    consulta.tratamento,
                    consulta.custo,
                    consulta.peso_registado,
                    consulta.estado
                )
            )

            consulta.id = cur.lastrowid

        return consulta

    def listar_por_animal(self, id_animal):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM consultas
                WHERE id_animal = ?
                ORDER BY horario
                """,
                (id_animal,)
            ).fetchall()

            return [
                Consulta(
                    id_animal=r["id_animal"],
                    cedula_profissional=r["cedula_profissional"],
                    horario=datetime.fromisoformat(r["horario"]),
                    diagnostico=r["diagnostico"],
                    tratamento=r["tratamento"],
                    custo=r["custo"],
                    peso_registado=r["peso_registado"],
                    estado=r["estado"]
                )
                for r in rows
            ]

    def cancelar(self, id_consulta):
        with get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE consultas
                SET estado = ?
                WHERE id = ?
                """,
                ("Cancelada", id_consulta)
            )

            return cur.rowcount > 0
        