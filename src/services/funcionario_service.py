"""src/services/funcionario_service.py"""

import bcrypt
import pyotp

from src.models.funcionario import Funcionario
from src.models.proprietario import Proprietario
from src.repositories.funcionario_repository import FuncionarioRepository


class FuncionarioService:
    """Serviço de gestão de funcionários, autenticação bcrypt e MFA (TOTP)."""

    def __init__(self, repo: FuncionarioRepository):
        """Inicializa o serviço com o repositório de funcionários."""
        self._repo = repo

    def _gerar_hash(self, palavra_passe: str) -> str:
        """Gera hash seguro da palavra-passe com bcrypt (rounds=12)."""
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(palavra_passe.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def _validar_palavra_passe(
        self,
        palavra_passe: str,
        hash_guardado: str
    ) -> bool:
        """Valida a palavra-passe em tempo constante usando bcrypt.checkpw()."""
        if not hash_guardado:
            return False

        hash_bytes = (
            hash_guardado.encode("utf-8")
            if isinstance(hash_guardado, str)
            else hash_guardado
        )

        try:
            return bcrypt.checkpw(palavra_passe.encode("utf-8"), hash_bytes)
        except ValueError:
            return False

    def _validar_proprietario(self, utilizador_atual):
        """Garante que a operação é executada por um proprietário ativo."""
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
        """Regista um novo funcionário com palavra-passe hasheada via bcrypt."""
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
        """Autentica um funcionário verificando estado ativo e hash bcrypt."""
        funcionario = self._repo.obter_por_nome_utilizador(
            nome_utilizador.strip()
        )

        if funcionario is None:
            # Executa verificação fictícia para mitigar enumeração de utilizadores
            bcrypt.checkpw(
                b"dummy",
                bcrypt.hashpw(b"dummy", bcrypt.gensalt(4))
            )
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

    def configurar_mfa(self, nome_utilizador: str) -> dict:
        """Gera e guarda o segredo TOTP para contas de Proprietário (Lab 3)."""
        utilizador_limpo = (nome_utilizador or "").strip()
        funcionario = self._repo.obter_por_nome_utilizador(utilizador_limpo)

        if funcionario is None:
            raise ValueError("Funcionário não encontrado.")

        if not isinstance(funcionario, Proprietario):
            raise ValueError(
                "A configuração MFA TOTP destina-se a contas de Proprietário."
            )

        segredo = pyotp.random_base32()
        self._repo.guardar_mfa_secret(utilizador_limpo, segredo)

        uri = pyotp.TOTP(segredo).provisioning_uri(
            name=utilizador_limpo,
            issuer_name="VetAmigos"
        )

        return {
            "secret": segredo,
            "uri": uri
        }

    def verificar_mfa(self, nome_utilizador: str, codigo: str) -> bool:
        """Valida o código TOTP (6 dígitos) do utilizador indicado (Lab 3)."""
        utilizador_limpo = (nome_utilizador or "").strip()
        segredo = self._repo.obter_mfa_secret(utilizador_limpo)

        # Se ainda não houver segredo configurado, permite prosseguir
        if not segredo:
            return True

        codigo_limpo = (codigo or "").strip()
        if not codigo_limpo:
            return False

        return pyotp.TOTP(segredo).verify(codigo_limpo, valid_window=1)

    def listar_todos(self):
        """Lista todos os funcionários registados."""
        return self._repo.listar_todos()

    def registar_por_proprietario(
        self,
        funcionario,
        palavra_passe,
        utilizador_atual
    ):
        """Regista um funcionário exigindo permissão de proprietário."""
        self._validar_proprietario(utilizador_atual)

        return self.registar(
            funcionario,
            palavra_passe
        )

    def listar_por_proprietario(self, utilizador_atual):
        """Lista todos os funcionários exigindo permissão de proprietário."""
        self._validar_proprietario(utilizador_atual)

        return self._repo.listar_todos()

    def desativar_por_proprietario(
        self,
        id_funcionario,
        utilizador_atual
    ):
        """Desativa um funcionário aplicando regras de segurança e integridade."""
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
        """Reativa um funcionário previamente desativado."""
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