"""Controlador de autenticação e MFA."""

from src.services import mfa_service


class AuthController:
    """Coordena autenticação e verificação multifator."""

    def __init__(self, funcionario_service):
        """Inicializa o controller com o serviço de funcionários."""
        self.service = funcionario_service

    def iniciar_sessao(self, utilizador, palavra_passe):
        """Valida a palavra-passe utilizando o serviço existente."""
        return self.service.iniciar_sessao(
            utilizador, palavra_passe
        )

    def registar(self, *args, **kwargs):
        """Impede registos de funcionários sem autorização."""
        raise PermissionError(
            "Utilize o FuncionarioController para registar funcionários."
        )

    def configurar_mfa(self, nome_utilizador):
        """Inicia a configuração TOTP do proprietário."""
        return mfa_service.iniciar_configuracao(nome_utilizador)

    def verificar_mfa(self, nome_utilizador, codigo):
        """Valida um código ou confirma a primeira configuração."""
        if mfa_service.mfa_ativo(nome_utilizador):
            return mfa_service.verificar_codigo(
                nome_utilizador, codigo
            )

        return mfa_service.confirmar_configuracao(
            nome_utilizador, codigo
        )