"""src/services/cliente_service.py"""

from src.models.cliente import Cliente
from src.repositories.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def _validar_nif_portugues(self, nif: str) -> bool:
        """Valida se o NIF português possui 9 dígitos numéricos (RNF13)."""
        return len(nif) == 9 and nif.isdigit()

    def registar(self, nome: str, nif: str, telefone: str, email: str) -> Cliente:
        """
        Aplica as regras de negócio e validações para registar um novo cliente (US-01 / RF01 / RNF13).
        """
        # Validação 1: Campos não vazios
        if not nome or not nome.strip():
            raise ValueError("O nome do cliente não pode estar vazio.")
        if not telefone or not telefone.strip():
            raise ValueError("O contacto telefónico é obrigatório.")
        if not email or not email.strip():
            raise ValueError("O email é obrigatório.")

        telefone_limpo = telefone.strip()
        email_limpo = email.strip()
        if len(telefone_limpo) != 9 or not telefone_limpo.isascii() or not telefone_limpo.isdigit():
            raise ValueError("O telefone deve conter exatamente 9 dígitos numéricos.")
        if "@" not in email_limpo:
            raise ValueError("O email deve conter pelo menos um @.")

        # Validação 2: Formato do NIF (RNF13)
        nif_limpo = nif.strip()
        if not self._validar_nif_portugues(nif_limpo):
            raise ValueError("NIF inválido. Deve possuir exatamente 9 dígitos numéricos.")

        # Validação 3: Unicidade do NIF (RNF13)
        if self._repo.obter_por_nif(nif_limpo) is not None:
            raise ValueError("Já existe um cliente registado com este NIF.")

        # Criação do objeto e persistência
        cliente = Cliente(nome=nome.strip(), nif=nif_limpo, telefone=telefone_limpo, email=email_limpo)
        return self._repo.inserir(cliente)

    def listar(self) -> list[Cliente]:
        """Obtém a lista de todos os clientes registados."""
        return self._repo.listar_todos()
