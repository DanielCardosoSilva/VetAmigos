"""src/services/registo_vacina_service.py"""

from datetime import date
from src.models.registo_vacina import RegistoVacina
from src.repositories.registo_vacina_repository import RegistoVacinaRepository


class RegistoVacinaService:
    def __init__(self, repo: RegistoVacinaRepository, animal_repo):
        self._repo = repo
        self._animal_repo = animal_repo

    def registar(self, id_animal: int, nome_vacina: str, data_administracao: date, data_proxima_dose: date = None) -> RegistoVacina:
        """Valida e regista a administração de uma vacina a um animal."""

        if self._animal_repo.obter_por_id(id_animal) is None:
            raise ValueError("Animal não encontrado.")

        if not nome_vacina or not nome_vacina.strip():
            raise ValueError("O nome da vacina é obrigatório.")

        if not isinstance(data_administracao, date):
            raise ValueError("A data de administração é inválida.")

        if data_administracao > date.today():
            raise ValueError("A data de administração não pode ser futura.")

        if data_proxima_dose is not None:
            if not isinstance(data_proxima_dose, date):
                raise ValueError("A data da próxima dose é inválida.")

            if data_proxima_dose <= data_administracao:
                raise ValueError("A próxima dose deve ter uma data posterior à administração.")

        registo = RegistoVacina(
            id_animal=id_animal,
            nome_vacina=nome_vacina.strip(),
            data_administracao=data_administracao,
            data_proxima_dose=data_proxima_dose
        )

        return self._repo.inserir(registo)

    def listar_por_animal(self, id_animal: int) -> list[RegistoVacina]:
        """Obtém o histórico de vacinação de um animal."""

        if self._animal_repo.obter_por_id(id_animal) is None:
            raise ValueError("Animal não encontrado.")

        return self._repo.listar_por_animal(id_animal)

    def listar_todos(self) -> list[RegistoVacina]:
        """Obtém todos os registos de vacinação."""
        return self._repo.listar_todos()
