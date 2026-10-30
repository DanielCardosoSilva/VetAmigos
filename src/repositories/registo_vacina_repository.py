"""src/repositories/registo_vacina_repository.py"""

from db.connection import get_connection
from src.models.registo_vacina import RegistoVacina
from datetime import date


class RegistoVacinaRepository:
    def inserir(self, registo: RegistoVacina) -> RegistoVacina:
        """Insere um registo de vacinação na base de dados."""
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO registovacina (id_animal, nome_vacina, data_administracao, data_proxima_dose) VALUES (?, ?, ?, ?)",
                (registo.id_animal, registo.nome_vacina, registo.data_administracao.isoformat(), registo.data_proxima_dose.isoformat() if registo.data_proxima_dose else None)
            )
            registo.id = cur.lastrowid
        return registo

    def listar_por_animal(self, id_animal: int) -> list[RegistoVacina]:
        """Devolve os registos de vacinação de um animal."""
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM registovacina WHERE id_animal = ?",
                (id_animal,)
            ).fetchall()

        registos = [
            RegistoVacina(
                id_animal=r["id_animal"],
                nome_vacina=r["nome_vacina"],
                data_administracao=date.fromisoformat(r["data_administracao"]),
                data_proxima_dose=date.fromisoformat(r["data_proxima_dose"]) if r["data_proxima_dose"] else None
            ) for r in rows
        ]

        for i in range(len(rows)):
            registos[i].id = rows[i]["id"]

        return registos

    def listar_todos(self) -> list[RegistoVacina]:
        """Devolve todos os registos de vacinação."""
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM registovacina").fetchall()

        registos = [
            RegistoVacina(
                id_animal=r["id_animal"],
                nome_vacina=r["nome_vacina"],
                data_administracao=date.fromisoformat(r["data_administracao"]),
                data_proxima_dose=date.fromisoformat(r["data_proxima_dose"]) if r["data_proxima_dose"] else None
            ) for r in rows
        ]

        for i in range(len(rows)):
            registos[i].id = rows[i]["id"]

        return registos
