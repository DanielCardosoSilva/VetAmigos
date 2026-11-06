"""src/repositories/consulta_repository.py"""

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
                    estado, motivo, sumario, data_conclusao
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    consulta.id_animal,
                    consulta.cedula_profissional,
                    consulta.horario.isoformat(sep=" "),
                    consulta.diagnostico,
                    consulta.tratamento,
                    consulta.custo,
                    consulta.peso_registado,
                    consulta.estado, consulta.motivo, consulta.sumario,
                    consulta.data_conclusao.isoformat(sep=" ") if consulta.data_conclusao else None
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

        consultas = [
            Consulta(
                id_animal=r["id_animal"],
                cedula_profissional=r["cedula_profissional"],
                horario=datetime.fromisoformat(r["horario"]),
                diagnostico=r["diagnostico"],
                tratamento=r["tratamento"],
                custo=r["custo"],
                peso_registado=r["peso_registado"],
                estado=r["estado"],
                motivo=r["motivo"],
                sumario=r["sumario"],
                data_conclusao=datetime.fromisoformat(r["data_conclusao"]) if r["data_conclusao"] else None
            )
            for r in rows
        ]

        for i in range(len(rows)):
            consultas[i].id = rows[i]["id"]

        return consultas
    
    def obter_por_id(self, id_consulta):
        with get_connection() as conn:
            r = conn.execute(
            "SELECT * FROM consultas WHERE id = ?",
            (id_consulta,)
            ).fetchone()

        if r is None:
            return None

        consulta = Consulta(
            id_animal=r["id_animal"],
            cedula_profissional=r["cedula_profissional"],
            horario=datetime.fromisoformat(r["horario"]),
            diagnostico=r["diagnostico"],
            tratamento=r["tratamento"],
            custo=r["custo"],
            peso_registado=r["peso_registado"],
            estado=r["estado"],
                motivo=r["motivo"],
                sumario=r["sumario"],
                data_conclusao=datetime.fromisoformat(r["data_conclusao"]) if r["data_conclusao"] else None
        )
        consulta.id = r["id"]
        return consulta

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
        
    def concluir(self, id_consulta, cedula_profissional, diagnostico,
                 tratamento, sumario, custo, peso_registado, data_conclusao):
        """Atualiza a consulta e o peso do animal numa única transação."""
        with get_connection() as conn:
            cur = conn.execute(
                """UPDATE consultas SET diagnostico=?, tratamento=?, sumario=?, custo=?,
                   peso_registado=?, data_conclusao=?, estado='Concluída'
                   WHERE id=? AND cedula_profissional=? AND estado='Agendada'""",
                (diagnostico, tratamento, sumario, custo, peso_registado,
                 data_conclusao.isoformat(sep=" "), id_consulta, cedula_profissional)
            )
            if cur.rowcount != 1:
                return False
            conn.execute(
                """UPDATE animais SET peso_animal=?
                   WHERE id=(SELECT id_animal FROM consultas WHERE id=?)""",
                (peso_registado, id_consulta)
            )
            return True
