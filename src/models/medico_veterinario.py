"""src/models/medico_veterinario.py"""

from src.models.funcionario import Funcionario


class MedicoVeterinario(Funcionario):
    """Representa um médico veterinário da clínica."""

    def __init__(self, nome: str, nome_utilizador: str, palavra_passe_hash: str, cedula_profissional: str):
        super().__init__(nome, nome_utilizador, palavra_passe_hash)
        self.cedula_profissional = cedula_profissional

    def __str__(self) -> str:
        return (
            f"MedicoVeterinario({self.id}: {self.nome}, "
            f"Cédula: {self.cedula_profissional}, "
            f"Utilizador: {self.nome_utilizador})"
        )
