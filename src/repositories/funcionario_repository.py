
"""src/repositories/funcionario_repository.py"""

from db.connection import get_connection
from src.models.recepcionista import Rececionista
from src.models.medico_veterinario import MedicoVeterinario
from src.models.proprietario import Proprietario


class FuncionarioRepository:
    def inserir(self, funcionario):
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO funcionarios (nome, nome_utilizador, palavra_passe_hash, tipo, cedula_profissional) VALUES (?, ?, ?, ?, ?)",
                (funcionario.nome, funcionario.nome_utilizador, funcionario.palavra_passe_hash, funcionario.tipo, getattr(funcionario, "cedula_profissional", None))
            )
            funcionario.id = cur.lastrowid
        return funcionario

    def obter_por_id(self, id_funcionario):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM funcionarios WHERE id = ?", (id_funcionario,)
            ).fetchone()

        if row:
            return self._converter_funcionario(row)

        return None

    def obter_por_nome_utilizador(self, nome_utilizador):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM funcionarios WHERE nome_utilizador = ?",
                (nome_utilizador,)
            ).fetchone()

        if row:
            return self._converter_funcionario(row)

        return None

    def listar_todos(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM funcionarios").fetchall()

        return [self._converter_funcionario(r) for r in rows]

    def _converter_funcionario(self, row):
        if row["tipo"] == "Rececionista":
            funcionario = Rececionista(
                row["nome"], row["nome_utilizador"], row["palavra_passe_hash"]
            )
        elif row["tipo"] == "MedicoVeterinario":
            funcionario = MedicoVeterinario(
                row["nome"], row["nome_utilizador"], row["palavra_passe_hash"],
                row["cedula_profissional"]
            )
        elif row["tipo"] == "Proprietario":
            funcionario = Proprietario(
                row["nome"], row["nome_utilizador"], row["palavra_passe_hash"]
            )
        else:
            raise ValueError("Tipo de funcionário desconhecido.")

        funcionario.id = row["id"]
        return funcionario
