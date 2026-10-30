# src/services/cliente_service.py
from src.models.cliente import Cliente
from src.repositories.cliente_repository import ClienteRepository

class ClienteService:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def _validar_nif_portugues(self, nif: str) -> bool:
        """Valida se o NIF português possui 9 dígitos numéricos (RNF13)."""
        return len(nif) == 9 and nif.isdigit()

    def registar(self, nome: str, nif: str, telefone: str, email: str, morada: str) -> Cliente:
        """
        Alica as regras de negócio e validações para registar um novo cliente (US-01 / RF01 / RNF13).
        """
        # Validação 1: Campos não vazios
        if not nome or not nome.strip():
            raise ValueError("O nome do cliente não pode estar vazio.")
        if not telefone or not telefone.strip():
            raise ValueError("O contacto telefónico é obrigatório.")
        if not email or not email.strip():
            raise ValueError("O email é obrigatório.")
        if not morada or not morada.strip():
            raise ValueError("A morada é obrigatória.")

        # Validação 2: Formato do NIF (RNF13)
        nif_limpo = nif.strip()
        if not self._validar_nif_portugues(nif_limpo):
            raise ValueError("NIF inválido. Deve possuir exatamente 9 dígitos numéricos.")

        # Validação 3: Unicidade do NIF (RNF13)
        if self._repo.obter_por_nif(nif_limpo) is not None:
            raise ValueError("Já existe um cliente registado com este NIF.")

        # Criação do objeto e persistência
        cliente = Cliente(nome=nome.strip(), nif=nif_limpo, telefone=telefone.strip(), email=email.strip(), morada=morada.strip())
        return self._repo.inserir(cliente)

    def listar(self) -> list[Cliente]:
        """Obtém a lista de todos os clientes cadastrados."""
        return self._repo.listar_todos()