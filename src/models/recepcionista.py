"""src/models/recepcionista.py"""

from src.models.funcionario import Funcionario


class Rececionista(Funcionario):
    """Representa um rececionista da clínica."""

    def __str__(self) -> str:
        return (
            f"Rececionista({self.id}: {self.nome}, "
            f"Utilizador: {self.nome_utilizador})"
        )
