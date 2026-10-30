"""src/models/medicamento.py"""

class Medicamento:
    """
    Representa um medicamento no sistema VetAmigos.
    """

    def __init__(self, nome: str, tipo: str, dose: str, quantidade: int):
        self.id = None
        self.nome = nome
        self.tipo = tipo
        self.dose = dose
        self.quantidade = quantidade

    def __str__(self) -> str:
        return f"Medicamento({self.id}: {self.nome}, [{self.tipo}], {self.dose}, {self.quantidade})"
