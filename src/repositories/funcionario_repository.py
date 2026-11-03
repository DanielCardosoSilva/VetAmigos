"""src/repositories/funcionario_repository.py"""

from db.connection import get_connection

from src.models.recepcionista import Rececionista
from src.models.medico_veterinario import MedicoVeterinario
from src.models.proprietario import Proprietario


class FuncionarioRepository:

    def inserir(self, funcionario):
        with get_connection() as conn:
            cur = conn.execute(
                """
                INSERT INTO funcionarios (
                    nome,
                    nome_utilizador,
                    palavra_passe_hash,
                    tipo,
                    cedula_profissional,
                    ativo
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    funcionario.nome,
                    funcionario.nome_utilizador,
                    funcionario.palavra_passe_hash,
                    funcionario.tipo,
                    getattr(
                        funcionario, "cedula_profissional", None
                    ),
                    int(funcionario.ativo)
                )
            )

            funcionario.id = cur.lastrowid

        return funcionario

    def obter_por_id(self, id_funcionario):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM funcionarios WHERE id = ?",
                (id_funcionario,)
            ).fetchone()

        if row:
            return self._converter_funcionario(row)

        return None

    def obter_por_nome_utilizador(self, nome_utilizador):
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT *
                FROM funcionarios
                WHERE nome_utilizador = ?
                """,
                (nome_utilizador,)
            ).fetchone()

        if row:
            return self._converter_funcionario(row)

        return None

    def listar_todos(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM funcionarios ORDER BY id"
            ).fetchall()

        return [
            self._converter_funcionario(row)
            for row in rows
        ]

    def listar_ativos(self):
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT *
                FROM funcionarios
                WHERE ativo = 1
                ORDER BY id
                """
            ).fetchall()

        return [
            self._converter_funcionario(row)
            for row in rows
        ]

    def alterar_estado(self, id_funcionario, ativo):
        with get_connection() as conn:
            cur = conn.execute(
                """
                UPDATE funcionarios
                SET ativo = ?
                WHERE id = ?
                """,
                (int(ativo), id_funcionario)
            )

            return cur.rowcount > 0

    def _converter_funcionario(self, row):
        if row["tipo"] == "Rececionista":
            funcionario = Rececionista(
                row["nome"],
                row["nome_utilizador"],
                row["palavra_passe_hash"]
            )

        elif row["tipo"] == "MedicoVeterinario":
            funcionario = MedicoVeterinario(
                row["nome"],
                row["nome_utilizador"],
                row["palavra_passe_hash"],
                row["cedula_profissional"]
            )

        elif row["tipo"] == "Proprietario":
            funcionario = Proprietario(
                row["nome"],
                row["nome_utilizador"],
                row["palavra_passe_hash"]
            )

        else:
            raise ValueError(
                "Tipo de funcionário desconhecido."
            )

        funcionario.id = row["id"]
        funcionario.ativo = bool(row["ativo"])

        return funcionario
