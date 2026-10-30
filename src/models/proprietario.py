"""src/models/proprietario.py"""

from src.models.funcionario import Funcionario


class Proprietario(Funcionario):
    """Representa o proprietário da empresa."""

    def __str__(self) -> str:
        return (
            f"Proprietario({self.id}: {self.nome}, "
            f"Utilizador: {self.nome_utilizador})"
        )
