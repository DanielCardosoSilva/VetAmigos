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
            return animal

        return None
