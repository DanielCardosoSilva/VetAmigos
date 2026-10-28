# src/models/cliente.py

class Cliente:
    """
    Representa a entidade Cliente / Proprietário no sistema VetAmigos.
    Não contém chamadas SQL ou instruções print(), mantendo-se isolado 
    como modelo de domínio puro.
    """
    def __init__(self, nome: str, nif: str, telefone: str, email: str):
        self.id = None
        self.nome = nome
        self.nif = nif
        self.telefone = telefone
        self.email = email

    def __str__(self) -> str:
        """Devolve uma representação legível em string do objeto Cliente."""
        return f"Cliente({self.id}: {self.nome} — NIF: {self.nif} — Telefone: {self.telefone} — Email: {self.email})"