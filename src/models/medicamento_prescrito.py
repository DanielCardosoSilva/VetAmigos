"""src/models/medicamento_prescrito.py"""


class MedicamentoPrescrito:
    """
    Representa um medicamento associado a uma receita.
    Não contém chamadas SQL ou instruções print().
    """

    def __init__(self, id_receita: int, id_medicamento: int, quantidade: int, posologia: str):
        self.id = None
        self.id_receita = id_receita
        self.id_medicamento = id_medicamento
        self.quantidade = quantidade
        self.posologia = posologia

    def __str__(self) -> str:
        return (
            f"MedicamentoPrescrito({self.id}: "
            f"Receita: {self.id_receita}, "
            f"Medicamento: {self.id_medicamento}, "
            f"Quantidade: {self.quantidade}, "
            f"Posologia: {self.posologia})"
        )
