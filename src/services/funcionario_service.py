"""src/services/funcionario_service.py"""

import hashlib
import secrets

from src.models.funcionario import Funcionario
from src.models.proprietario import Proprietario
from src.repositories.funcionario_repository import FuncionarioRepository


class FuncionarioService:

    def __init__(self, repo: FuncionarioRepository):
        self._repo = repo

    def _gerar_hash(self, palavra_passe: str) -> str:
        salt = secrets.token_hex(16)

        hash_passe = hashlib.pbkdf2_hmac(
            "sha256",
            palavra_passe.encode(),
            salt.encode(),
            600000
        ).hex()

        return f"{salt}${hash_passe}"

    def _validar_palavra_passe(
        self,
        palavra_passe: str,
        hash_guardado: str
    ) -> bool:
        salt, hash_original = hash_guardado.split("$")

        hash_passe = hashlib.pbkdf2_hmac(
            "sha256",
            palavra_passe.encode(),
            salt.encode(),
            600000
        ).hex()

        return secrets.compare_digest(
            hash_passe,
            hash_original
        )

    def _validar_proprietario(self, utilizador_atual):
        if not isinstance(utilizador_atual, Proprietario):
            raise ValueError(
                "Apenas proprietários podem gerir funcionários."
            )

        if utilizador_atual.id is None:
            raise ValueError("Sessão inválida.")

        proprietario = self._repo.obter_por_id(
            utilizador_atual.id
        )

        if (
            proprietario is None
            or not isinstance(proprietario, Proprietario)
            or not proprietario.ativo
        ):
            raise ValueError(
                "O proprietário não tem uma conta ativa."
            )

    def registar(
        self,
        funcionario: Funcionario,
        palavra_passe: str
    ):
        if not funcionario.nome or not funcionario.nome.strip():
            raise ValueError("O nome é obrigatório.")

        if (
            not funcionario.nome_utilizador
            or not funcionario.nome_utilizador.strip()
        ):
            raise ValueError(
                "O nome de utilizador é obrigatório."
            )

        if not palavra_passe:
            raise ValueError(
                "A palavra-passe é obrigatória."
            )

        funcionario.nome = funcionario.nome.strip()
        funcionario.nome_utilizador = (
            funcionario.nome_utilizador.strip()
        )

        existente = self._repo.obter_por_nome_utilizador(
            funcionario.nome_utilizador
        )

        if existente is not None:
            raise ValueError(
                "Já existe um funcionário com esse nome "
                "de utilizador."
            )

        funcionario.palavra_passe_hash = (
            self._gerar_hash(palavra_passe)
        )

        funcionario.ativo = True

        return self._repo.inserir(funcionario)

    def iniciar_sessao(
        self,
        nome_utilizador: str,
        palavra_passe: str
    ):
        funcionario = self._repo.obter_por_nome_utilizador(
            nome_utilizador.strip()
        )

        if funcionario is None:
            raise ValueError(
                "Nome de utilizador ou palavra-passe incorretos."
            )

        if not funcionario.ativo:
            raise ValueError(
                "Esta conta está desativada. "
                "Contacte o proprietário."
            )

        if not self._validar_palavra_passe(
            palavra_passe,
            funcionario.palavra_passe_hash
        ):
            raise ValueError(
                "Nome de utilizador ou palavra-passe incorretos."
            )

        return funcionario

    def listar_todos(self):
        return self._repo.listar_todos()

    def registar_por_proprietario(
        self,
        funcionario,
        palavra_passe,
        utilizador_atual
    ):
        self._validar_proprietario(utilizador_atual)

        return self.registar(
            funcionario,
            palavra_passe
        )

    def listar_por_proprietario(self, utilizador_atual):
        self._validar_proprietario(utilizador_atual)

        return self._repo.listar_todos()

    def desativar_por_proprietario(
        self,
        id_funcionario,
        utilizador_atual
    ):
        self._validar_proprietario(utilizador_atual)

        funcionario = self._repo.obter_por_id(
            id_funcionario
        )

        if funcionario is None:
            raise ValueError(
                "Funcionário não encontrado."
            )

        if not funcionario.ativo:
            raise ValueError(
                "Este funcionário já está desativado."
            )

        if funcionario.id == utilizador_atual.id:
            raise ValueError(
                "Não pode desativar a sua própria conta."
            )

        if isinstance(funcionario, Proprietario):
            proprietarios_ativos = [
                f for f in self._repo.listar_ativos()
                if isinstance(f, Proprietario)
            ]

            if len(proprietarios_ativos) <= 1:
                raise ValueError(
                    "Não é possível desativar "
                    "o último proprietário ativo."
                )

        return self._repo.alterar_estado(
            id_funcionario,
            False
        )

    def reativar_por_proprietario(
        self,
        id_funcionario,
        utilizador_atual
    ):
        self._validar_proprietario(utilizador_atual)

        funcionario = self._repo.obter_por_id(
            id_funcionario
        )

        if funcionario is None:
            raise ValueError(
                "Funcionário não encontrado."
            )

        if funcionario.ativo:
            raise ValueError(
                "Este funcionário já está ativo."
            )

        return self._repo.alterar_estado(
            id_funcionario,
            True
        )
