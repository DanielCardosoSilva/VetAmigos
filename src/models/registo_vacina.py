"""src/models/registo_vacina.py"""

from datetime import date


class RegistoVacina:
    """
    Representa o registo da administração de uma vacina a um animal.
    """

    def __init__(self, id_animal: int, nome_vacina: str, data_administracao: date, data_proxima_dose: date):
        self.id = None
        self.id_animal = id_animal
        self.nome_vacina = nome_vacina
        self.data_administracao = data_administracao
        self.data_proxima_dose = data_proxima_dose

    def __str__(self) -> str:
        return (
            f"RegistoVacina({self.id}: "
            f"Animal: {self.id_animal}, "
            f"Vacina: {self.nome_vacina}, "
            f"Administração: {self.data_administracao}, "
            f"Próxima dose: {self.data_proxima_dose})"
        )
    