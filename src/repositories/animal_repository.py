"""src/repositories/animal_repository.py"""

from db.connection import get_connection
from src.models.animal import Animal
from datetime import date


class AnimalRepository:
    def inserir(self, animal):
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO animais (nome, especie, data_nasc, peso_animal, nif_cliente)"
                " VALUES (?,?,?,?,?)",
                (animal.nome, animal.especie, animal.data_nasc.isoformat(), animal.peso_animal, animal.nif_cliente)
            )
            animal.id = cur.lastrowid
        return animal

    def listar_todos(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM animais").fetchall()

        animais = [
            Animal(
                nome=r["nome"],
                especie=r["especie"],
                data_nasc=date.fromisoformat(r["data_nasc"]),
                peso_animal=r["peso_animal"],
                nif_cliente=r["nif_cliente"]
            )
            for r in rows
        ]

        for i in range(len(rows)):
            animais[i].id = rows[i]["id"]
            animais[i].ativo = bool(rows[i]["ativo"])

        return animais

    def obter_por_id(self, id_animal: int) -> Animal | None:
        """Obtém um animal através do seu ID."""
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM animais WHERE id = ?", (id_animal,)
            ).fetchone()

        if row:
            animal = Animal(
                nome=row["nome"],
                especie=row["especie"],
                data_nasc=date.fromisoformat(row["data_nasc"]),
                peso_animal=row["peso_animal"],
                nif_cliente=row["nif_cliente"]
            )
            animal.id = row["id"]
            animal.ativo = bool(row["ativo"])
            return animal

        return None

    def atualizar_peso(self, id_animal: int, novo_peso: float) -> bool:
        with get_connection() as conn:
            cur = conn.execute("UPDATE animais SET peso_animal = ? WHERE id = ?", (novo_peso, id_animal))
            return cur.rowcount > 0

    def atualizar(self, animal: Animal) -> bool:
        """Atualiza os dados do animal sem alterar o seu identificador."""
        with get_connection() as conn:
            cur = conn.execute(
                """UPDATE animais SET nome = ?, especie = ?, data_nasc = ?,
                   peso_animal = ?, nif_cliente = ? WHERE id = ?""",
                (animal.nome, animal.especie, animal.data_nasc.isoformat(),
                 animal.peso_animal, animal.nif_cliente, animal.id)
            )
            return cur.rowcount > 0

    def definir_ativo(self, id_animal: int, ativo: bool) -> bool:
        """Arquiva ou reativa o animal sem apagar consultas e vacinas."""
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE animais SET ativo = ? WHERE id = ?",
                (int(ativo), id_animal)
            )
            return cur.rowcount > 0

    def tem_consultas_futuras(self, id_animal: int) -> bool:
        """Verifica se existem consultas agendadas em datas futuras."""
        from datetime import datetime
        with get_connection() as conn:
            return conn.execute(
                """SELECT 1 FROM consultas WHERE id_animal = ?
                   AND estado = 'Agendada' AND horario >= ? LIMIT 1""",
                (id_animal, datetime.now().isoformat())
            ).fetchone() is not None
