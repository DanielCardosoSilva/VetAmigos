from datetime import date

class Receita:
    """
    Representa a Receita médica associada a uma consulta (US-09 / RF10).
    """
    def __init__(self, id_consulta: int, data_emissao: date, id: int = None):
        self.id = id
        self.id_consulta = id_consulta
        self.data_emissao = data_emissao

    def __str__(self) -> str:
        return f"Receita(id: {self.id} — Consulta ID: {self.id_consulta} — Data: {self.data_emissao})"