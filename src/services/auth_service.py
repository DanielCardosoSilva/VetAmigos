"""src/services/auth_service.py"""

import bcrypt
import pyotp

from src.models.funcionario import Funcionario
from src.repositories.funcionario_repository import FuncionarioRepository


class AuthService:
    """Serviço de autenticação, hashing bcrypt e MFA (TOTP) para o VetAmigos."""

    def __init__(self, repo: FuncionarioRepository):
        """Inicializa o serviço com o repositório de funcionários."""
        self._repo = repo

    def registar(
        self,
        nome: str,
        utilizador: str,
        senha: str,
        tipo: str,
        cedula=None
    ):
        """Regista funcionário com palavra-passe hasheada com bcrypt (rounds=12)."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(senha.encode("utf-8"), salt)
        # Armazena como string UTF-8 na BD (ou bytes, convertendo na verificação)
        hashed_str = hashed.decode("utf-8")

        func = Funcionario(nome, utilizador, hashed_str, tipo, cedula)
        return self._repo.inserir(func)

    def iniciar_sessao(self, nome_utilizador: str, senha: str):
        """Autentica funcionário. Devolve o objeto funcionário ou lança ValueError."""
        func = self._repo.obter_por_nome_utilizador(nome_utilizador)

        if func is None:
            # Comparação em tempo constante para reduzir enumeração de utilizadores
            bcrypt.checkpw(b"dummy", bcrypt.hashpw(b"dummy", bcrypt.gensalt(4)))
            raise ValueError("Credenciais inválidas.")

        hash_armazenado = func.palavra_passe_hash
        if isinstance(hash_armazenado, str):
            hash_armazenado = hash_armazenado.encode("utf-8")

        try:
            senha_valida = bcrypt.checkpw(senha.encode("utf-8"), hash_armazenado)
        except ValueError:
            senha_valida = False

        if not senha_valida:
            raise ValueError("Credenciais inválidas.")

        if not getattr(func, "ativo", True):
            raise ValueError("Conta desactivada.")

        return func

    def configurar_mfa(self, nome_utilizador: str) -> dict:
        """Gera e guarda segredo TOTP para o Proprietário (Lab 3)."""
        func = self._repo.obter_por_nome_utilizador(nome_utilizador)
        if func is None:
            raise ValueError("Utilizador não encontrado.")

        segredo = pyotp.random_base32()
        self._repo.guardar_mfa_secret(nome_utilizador, segredo)
        uri = pyotp.TOTP(segredo).provisioning_uri(
            name=nome_utilizador,
            issuer_name="VetAmigos"
        )
        return {"secret": segredo, "uri": uri}

    def verificar_mfa(self, nome_utilizador: str, codigo: str) -> bool:
        """Valida o código TOTP (6 dígitos) para o utilizador indicado (Lab 3)."""
        segredo = self._repo.obter_mfa_secret(nome_utilizador)
        if not segredo:
            # MFA ainda não configurado: permite acesso ou força configuração na vista
            return True

        codigo_limpo = (codigo or "").strip()
        if not codigo_limpo:
            return False

        return pyotp.TOTP(segredo).verify(codigo_limpo, valid_window=1)