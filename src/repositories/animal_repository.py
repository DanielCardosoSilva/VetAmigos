class AnimalRepository:
    def inserir(self, animal):
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO animais (nome, especie, data_nasc, peso_animal, nif_cliente, id=None)"
                " VALUES (?,?,?,?,?,?)",
                (animal.nome, animal.especie, animal.data_nasc, animal.peso_animal, animal.nif_cliente, animal.id)
            )
        return animal

    def listar_todos(self):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM animais").fetchall()
        return [
            Animal(
                id=r[id]
                nome=r[nome],
                especie=r[especie],
                data_nasc=date.fromisoformat(r[data_nasc]),
                nif_cliente=r[nif_cliente],
            ) for r in rows
        ]
