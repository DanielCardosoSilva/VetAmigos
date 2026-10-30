"""src/models/receita.py"""

from datetime import date


class Receita:
    """
    Representa uma receita médica associada a uma consulta.
    """

    def __init__(self, id_consulta: int, data_emissao: date):
        self.id = None
        self.id_consulta = id_consulta
        self.data_emissao = data_emissao

    def __str__(self) -> str:
        return (
            f"Receita({self.id}: "
            f"Consulta ID: {self.id_consulta}, "
            f"Data: {self.data_emissao})"
        )
    