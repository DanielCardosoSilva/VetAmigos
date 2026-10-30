
"""src/services/funcionario_service.py"""

import hashlib
import secrets

from src.models.funcionario import Funcionario
from src.repositories.funcionario_repository import FuncionarioRepository


class FuncionarioService:
    def __init__(self, repo: FuncionarioRepository):
        self._repo = repo

    def _gerar_hash(self, palavra_passe: str) -> str:
        salt = secrets.token_hex(16)
        hash_passe = hashlib.pbkdf2_hmac(
            "sha256", palavra_passe.encode(), salt.encode(), 600000
        ).hex()

        return f"{salt}${hash_passe}"

    def _validar_palavra_passe(self, palavra_passe: str, hash_guardado: str) -> bool:
        salt, hash_original = hash_guardado.split("$")

        hash_passe = hashlib.pbkdf2_hmac(
            "sha256", palavra_passe.encode(), salt.encode(), 600000
        ).hex()

        return secrets.compare_digest(hash_passe, hash_original)

    def registar(self, funcionario: Funcionario, palavra_passe: str):
        """Regista um funcionário após validar os dados."""

        if not funcionario.nome or not funcionario.nome.strip():
            raise ValueError("O nome é obrigatório.")

        if not funcionario.nome_utilizador or not funcionario.nome_utilizador.strip():
            raise ValueError("O nome de utilizador é obrigatório.")

        if not palavra_passe:
            raise ValueError("A palavra-passe é obrigatória.")

        if self._repo.obter_por_nome_utilizador(funcionario.nome_utilizador.strip()) is not None:
            raise ValueError("Já existe um funcionário com esse nome de utilizador.")

        funcionario.nome = funcionario.nome.strip()
        funcionario.nome_utilizador = funcionario.nome_utilizador.strip()
        funcionario.palavra_passe_hash = self._gerar_hash(palavra_passe)

        return self._repo.inserir(funcionario)

    def iniciar_sessao(self, nome_utilizador: str, palavra_passe: str):
        """Valida as credenciais e inicia a sessão do funcionário."""

        funcionario = self._repo.obter_por_nome_utilizador(nome_utilizador.strip())

        if funcionario is None:
            raise ValueError("Nome de utilizador ou palavra-passe incorretos.")

        if not self._validar_palavra_passe(palavra_passe, funcionario.palavra_passe_hash):
            raise ValueError("Nome de utilizador ou palavra-passe incorretos.")

        return funcionario

    def listar_todos(self):
        return self._repo.listar_todos()
