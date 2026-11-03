
"""src/models/funcionario.py"""


class Funcionario:
    """
    Representa um funcionário do sistema VetAmigos.
    Classe parental de Rececionista, MedicoVeterinario
    e Proprietario.
    """

    def __init__(
        self,
        nome: str,
        nome_utilizador: str,
        palavra_passe_hash: str
    ):
        self.id = None
        self.nome = nome
        self.nome_utilizador = nome_utilizador
        self.palavra_passe_hash = palavra_passe_hash
        self.tipo = self.__class__.__name__
        self.ativo = True

    def __str__(self) -> str:
        estado = "Ativo" if self.ativo else "Inativo"

        return (
            f"Funcionario({self.id}: {self.nome}, "
            f"Utilizador: {self.nome_utilizador}, "
            f"Perfil: {self.tipo}, Estado: {estado})"
        )
